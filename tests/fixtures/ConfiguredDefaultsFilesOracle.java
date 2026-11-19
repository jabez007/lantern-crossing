// Isolated adapter for the pinned, unmodified upstream file handler.
// Requires the game directory as both argument and working directory.
// No Fabric loader, Minecraft initialization or launcher is executed.
import java.nio.file.Path;
import fuzs.configureddefaults.common.handler.CopyDefaultsHandler;

public class ConfiguredDefaultsFilesOracle {
    public static void main(String[] args) {
        CopyDefaultsHandler.initialize(Path.of(args[0]), true);
    }
}
