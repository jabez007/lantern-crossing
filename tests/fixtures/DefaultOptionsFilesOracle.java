// File-handling adapter only. Compile against the pinned upstream handler source.
// Minecraft-dependent initialization, key mappings and resource repositories are
// not executed. See docs/configuration.md for the scope and observed fixtures.
import java.io.File;
import net.blay09.mods.defaultoptions.DefaultOptionsContext;
import net.blay09.mods.defaultoptions.ExtraDefaultOptionsHandler;
import net.blay09.mods.defaultoptions.SimpleDefaultOptionsFileHandler;

public class DefaultOptionsFilesOracle {
    public static void main(String[] args) throws Exception {
        var context = new DefaultOptionsContext(new File(args[0]));
        var options = new SimpleDefaultOptionsFileHandler(new File("options.txt"));
        options.withLinePredicate(line -> !line.startsWith("key_"));
        if (options.shouldLoadDefaults(context)) {
            options.loadDefaults(context);
        }
        new ExtraDefaultOptionsHandler().loadDefaults(context);
    }
}
