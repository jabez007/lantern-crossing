import java.io.*;
import java.util.*;
import net.fabricmc.loader.api.Version;
import net.fabricmc.loader.api.metadata.version.VersionPredicate;
public class PredicateOracle {
 public static void main(String[] args) throws Exception {
  BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
  String line;
  while ((line = input.readLine()) != null) {
   String[] parts = line.split("\t", -1);
   try {
    Version version = Version.parse(parts[0]);
    boolean result = false;
    for (String predicate : parts[1].split("\u001f", -1)) {
     result |= VersionPredicate.parse(predicate).test(version);
    }
    System.out.println(result);
   } catch (Exception e) { System.out.println("invalid"); }
  }
 }
}
