"""Check pinned native Fabric requirements without replacing Loader's SAT resolver."""

from functools import cmp_to_key

from fabric_versions import UnsupportedPredicate, compare, parse_version, predicates, satisfies


def installed_versions(groups: dict, runtime: dict[str, str]) -> dict[str, set[str]]:
    inventory = {name: {value} for name, value in runtime.items()}
    for group in groups.values():
        for module in group:
            for name in [module["id"], *module.get("provides", [])]:
                if name in runtime:
                    raise ValueError(f"mod attempts to provide reserved runtime ID: {name}")
                inventory.setdefault(name, set()).add(module["version"])
    return inventory


def mandatory_versions(groups: dict, runtime: dict[str, str]) -> dict[str, str]:
    result = dict(runtime)
    for group in groups.values():
        root = group[0]
        for name in [root["id"], *root.get("provides", [])]:
            if name in result:
                raise UnsupportedPredicate(f"duplicate mandatory Fabric ID or alias: {name}")
            result[name] = root["version"]
    return result


def preferred_version(available: set[str]) -> str:
    # Build metadata does not affect Fabric ordering. Sort text first for stable ties.
    return max(
        sorted(available), key=cmp_to_key(lambda a, b: compare(parse_version(a), parse_version(b)))
    )


def check_relation(module, dependency, expression, inventory, selected, mandatory, breaking):
    relation = "breaks" if breaking else "requires"
    label = f"{module['id']}@{module['version']} {relation} {dependency} {expression!r}"
    try:
        predicates(expression)
        available = inventory.get(dependency)
        if not available:
            if not breaking:
                raise ValueError(f"{label}; installed version: MISSING")
            return
        installed = selected[dependency]
        matches = satisfies(installed, expression)
        if matches == breaking:
            alternatives = [v for v in available if satisfies(v, expression) != breaking]
            if alternatives and dependency not in mandatory:
                raise UnsupportedPredicate(
                    f"bundled alternatives {sorted(available)!r} need Loader resolution"
                )
            raise ValueError(f"{label}; installed version: {installed}")
    except UnsupportedPredicate as error:
        raise UnsupportedPredicate(f"{label}; unsupported/unevaluable: {error}") from error


def validate_native_dependencies(groups: dict, runtime: dict[str, str]) -> None:
    """Consume pack_model's existing flattened root/bundle groups."""
    inventory = installed_versions(groups, runtime)
    mandatory = mandatory_versions(groups, runtime)
    selected = {
        name: mandatory[name] if name in mandatory else preferred_version(available)
        for name, available in inventory.items()
    }
    for group in groups.values():
        for module in group:
            preferred = parse_version(selected[module["id"]])
            own = parse_version(module["version"])
            if preferred.components is None or own.components is None:
                active = preferred.text == own.text
            else:
                active = compare(preferred, own) == 0
            if not active:
                continue  # A newer bundled copy supplies this Fabric ID.
            for dependency, expression in module.get("depends", {}).items():
                check_relation(
                    module, dependency, expression, inventory, selected, mandatory, False
                )
            for dependency, expression in module.get("breaks", {}).items():
                check_relation(module, dependency, expression, inventory, selected, mandatory, True)
            # recommends/suggests/conflicts are soft declarations, not required edges.
