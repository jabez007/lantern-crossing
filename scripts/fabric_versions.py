"""Conservative offline predicates following Fabric Loader 0.20.1, not npm SemVer.

Supports extended numeric versions, opaque equality, AND strings, OR arrays,
comparisons, caret, tilde and trailing wildcards. Unsupported syntax fails closed.
This evaluates predicates, not Fabric's complete mod-selection/SAT algorithm.
"""

import re
from dataclasses import dataclass
from functools import lru_cache
from itertools import zip_longest


class UnsupportedPredicate(ValueError):
    """The declaration cannot be evaluated safely by this offline implementation."""


@dataclass(frozen=True)
class Version:
    text: str
    components: tuple[int, ...] | None
    prerelease: str | None = None


@lru_cache(maxsize=4096)
def parse_version(text: str) -> Version:
    if not isinstance(text, str) or not text:
        raise UnsupportedPredicate("version must be a nonempty string")
    core, plus, build = text.partition("+")
    core, dash, prerelease = core.partition("-")
    if not core.isascii():
        raise UnsupportedPredicate("non-ASCII version cores require Loader evaluation")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", core):
        return Version(text, None)
    if dash and not re.fullmatch(r"(?:[-0-9A-Za-z]+(?:\.[-0-9A-Za-z]+)*)?", prerelease):
        return Version(text, None)
    components = tuple(int(part) for part in core.split("."))
    if any(part > 2147483647 for part in components):
        return Version(text, None)
    friendly = ".".join(str(part) for part in components)
    friendly += ("-" + prerelease) if dash else ""
    friendly += ("+" + build) if plus else ""
    return Version(friendly, components, prerelease if dash else None)


def compare_identifier(left: str, right: str) -> int:
    numeric_left = bool(re.fullmatch(r"0|[1-9][0-9]*", left))
    numeric_right = bool(re.fullmatch(r"0|[1-9][0-9]*", right))
    if numeric_left != numeric_right:
        return -1 if numeric_left else 1
    if numeric_left and len(left) != len(right):
        return (len(left) > len(right)) - (len(left) < len(right))
    return (left > right) - (left < right)


def compare(left: Version, right: Version) -> int:
    if left.components is None or right.components is None:
        if left.text == right.text:
            return 0
        raise UnsupportedPredicate("ordering opaque versions is not supported")
    for a, b in zip_longest(left.components, right.components, fillvalue=0):
        if a != b:
            return (a > b) - (a < b)
    if left.prerelease is None or right.prerelease is None:
        return (left.prerelease is None) - (right.prerelease is None)
    a_parts = left.prerelease.split(".") if left.prerelease else []
    b_parts = right.prerelease.split(".") if right.prerelease else []
    for a, b in zip(a_parts, b_parts):
        result = compare_identifier(a, b)
        if result:
            return result
    return (len(a_parts) > len(b_parts)) - (len(a_parts) < len(b_parts))


@dataclass(frozen=True)
class Term:
    operator: str
    reference: Version

    def matches(self, version: Version) -> bool:
        if version.components is None or self.reference.components is None:
            return self.operator not in {"<", ">"} and version.text == self.reference.text
        result = compare(version, self.reference)
        if self.operator in {"^", "~"}:
            width = 1 if self.operator == "^" else 2
            pairs = zip_longest(
                version.components[:width], self.reference.components[:width], fillvalue=0
            )
            return result >= 0 and all(a == b for a, b in pairs)
        return {
            "=": result == 0,
            ">": result > 0,
            ">=": result >= 0,
            "<": result < 0,
            "<=": result <= 0,
        }[self.operator]


def wildcard_terms(value: str, operator: str) -> tuple[Term, ...]:
    core = value.split("+", 1)[0]
    parts = core.split(".")
    prefix = []
    for part in parts:
        if part in {"x", "X", "*"}:
            break
        if not part.isascii() or not part.isdecimal():
            raise UnsupportedPredicate(f"invalid wildcard version: {value!r}")
        prefix.append(int(part))
    if (
        operator != "="
        or not prefix
        or any(p not in {"x", "X", "*"} for p in parts[len(prefix) :])
        or any(p >= 2147483647 for p in prefix)
    ):
        raise UnsupportedPredicate(f"unsupported wildcard predicate: {operator}{value}")
    lower = parse_version(".".join(map(str, prefix)) + "-")
    upper = parse_version(".".join(map(str, [*prefix[:-1], prefix[-1] + 1])) + "-")
    return (Term(">=", lower), Term("<", upper))


@lru_cache(maxsize=4096)
def parse_clause(expression: str) -> tuple[Term, ...]:
    if any(char in expression for char in "\t\r\n,|[]!"):
        raise UnsupportedPredicate(f"unsupported Fabric predicate syntax: {expression!r}")
    terms = []
    for token in expression.split(" "):
        token = token.strip()
        if token in {"", "*"}:
            continue
        match = re.fullmatch(r"(>=|<=|>|<|=|\^|~)?(.+)", token)
        if not match:
            raise UnsupportedPredicate(f"invalid Fabric predicate: {token!r}")
        operator, value = match.group(1) or "=", match.group(2)
        if value[0] in "><=^~":
            raise UnsupportedPredicate(f"invalid Fabric predicate: {token!r}")
        if any(part in {"x", "X", "*"} for part in value.split("+", 1)[0].split(".")):
            terms.extend(wildcard_terms(value, operator))
            continue
        reference = parse_version(value)
        if reference.components is None and operator in {"<", ">"}:
            raise UnsupportedPredicate(f"exclusive bound needs a numeric version: {token!r}")
        terms.append(Term(operator if reference.components is not None else "=", reference))
    return tuple(terms)


def predicates(expression: str | list[str]) -> tuple[tuple[Term, ...], ...]:
    alternatives = [expression] if isinstance(expression, str) else expression
    if not isinstance(alternatives, list) or not alternatives:
        raise UnsupportedPredicate("predicate must be a string or a nonempty OR array")
    if not all(isinstance(part, str) for part in alternatives):
        raise UnsupportedPredicate("predicate alternatives must be strings")
    # Parse every alternative before testing, so an OR match cannot hide bad syntax.
    return tuple(parse_clause(part) for part in alternatives)


def satisfies(version: str, expression: str | list[str]) -> bool:
    parsed = parse_version(version)
    return any(all(term.matches(parsed) for term in terms) for terms in predicates(expression))
