// Run against unmodified FontProcessor, MappedFontProcessor and Util sources.
// Only Minecraft identifier, translation and GsonHelper adapters are stubbed.
// Uses the real Gson/ICU libraries and font JSON from the SHA-512-checked JAR.
import com.google.gson.*;
import java.nio.file.*;
import net.minecraft.resources.Identifier;
import net.replaceitem.symbolchat.resource.MappedFontProcessor;

public class SymbolChatFontsOracle {
    public static void main(String[] args) throws Exception {
        JsonArray results = new JsonArray();
        for (String name : new String[]{"mathematical_bold", "fullwidth", "circled"}) {
            Path path = Path.of(args[0], name + ".json");
            JsonObject definition = JsonParser.parseString(Files.readString(path)).getAsJsonObject();
            var font = MappedFontProcessor.read(new Identifier(), definition, 0, false);
            String input = "Az09 / Oak 🌿";
            String output = font.convertString(input);
            if (!font.convertString("🌿").equals("🌿") || output.contains("§"))
                throw new AssertionError("Unmapped supplementary text must survive without formatting codes");
            JsonObject result = new JsonObject();
            result.addProperty("font", name);
            result.addProperty("input", input);
            result.addProperty("output", output);
            results.add(result);
        }
        System.out.println(new GsonBuilder().disableHtmlEscaping().setPrettyPrinting().create().toJson(results));
    }
}
