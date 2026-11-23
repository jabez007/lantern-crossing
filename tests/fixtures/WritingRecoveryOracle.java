package me.devjg.booker.mixin;

import com.google.gson.*;
import com.bookextractor.export.BookExportFormatter;
import com.bookextractor.model.*;
import ru.svyaton.bookpaste.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import java.lang.reflect.*;
import java.time.LocalDateTime;
import java.util.*;

// Executes unmodified candidate JAR classes. Framework/config adapters are stubs.
// The fitter below measures UTF-16 capacity, not Minecraft's rendered layout.
public class WritingRecoveryOracle {
    private static final JsonObject RESULTS = new JsonObject();

    private static void require(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }

    private static void pasteCases() {
        JsonObject cases = new JsonObject();
        PasteHelper.PageFitter fits = text -> text.length() <= 1024;
        var longWord = PasteHelper.buildPage("", "x".repeat(1100), fits, false);
        require(longWord.pageText().length() == 1024 && longWord.remainingText().length() == 76, "long word remainder");
        cases.addProperty("long-word-remainder-units", longWord.remainingText().length());
        var full = PasteHelper.buildPage("x".repeat(1024), "next", fits, true);
        require(full.remainingText().equals("next"), "full final page must retain remainder");
        cases.addProperty("full-final-page-retains-text", full.remainingText().equals("next"));
        var last = PasteHelper.buildPage("x".repeat(1023), "XY", fits, true);
        require(last.pageText().endsWith("X") && last.remainingText().equals("Y"), "partial final page");
        cases.addProperty("partial-final-page-remainder", last.remainingText());
        var pair = PasteHelper.buildPage("x".repeat(1023), "🌿Z", fits, true);
        require(pair.remainingText().equals("🌿Z"), "surrogate boundary");
        cases.addProperty("surrogate-pair-preserved-at-capacity", true);
        var combining = PasteHelper.buildPage("x".repeat(1023), "e\u0301Z", fits, true);
        require(combining.pageText().endsWith("e") && combining.remainingText().equals("\u0301Z"), "combining sequence boundary finding");
        cases.addProperty("combining-sequence-remainder", combining.remainingText());
        for (PasteFormatMode mode : PasteFormatMode.values()) {
            BookPasteConfigManager.getConfig().setFormatMode(mode);
            var whitespace = PasteHelper.buildPage("", "alpha\n\n", fits, false);
            cases.addProperty(mode.name() + "-whitespace-output", whitespace.pageText() + whitespace.remainingText());
            require(!"alpha\n\n".equals(whitespace.pageText() + whitespace.remainingText()), "expected whitespace loss finding");
        }
        BookPasteConfigManager.getConfig().setFormatMode(PasteFormatMode.SMART_FILL);
        var boundary = PasteHelper.buildPage("", "abcdefgh \n\nnext", text -> text.length() <= 8, false);
        cases.addProperty("boundary-output", boundary.pageText());
        cases.addProperty("boundary-remainder", boundary.remainingText());
        String huge = "x".repeat(500000);
        for (int i = 0; i < 100; i++) huge = PasteHelper.buildPage("", huge, fits, i == 99).remainingText();
        require(huge.length() == 397600, "100 helper slices preserve large remainder");
        cases.addProperty("large-payload-remainder-after-100-helper-slices", huge.length());
        RESULTS.add("bookpaste", cases);
    }

    @SuppressWarnings("unchecked")
    private static void extractorCases() throws Exception {
        Class<?> service = Class.forName("com.bookextractor.client.BookImportService");
        Method parse = service.getDeclaredMethod("parsePages", String.class);
        Method validate = service.getDeclaredMethod("validatePages", List.class);
        parse.setAccessible(true);
        validate.setAccessible(true);
        JsonObject cases = new JsonObject();
        List<String> original = List.of("  alpha\n\n", "", "🌿 café");
        var book = new ExtractedBook(BookType.WRITABLE, "fixture", "fixture", original, BookSource.BOOK_AND_QUILL);
        List<String> parsed = (List<String>) parse.invoke(null, BookExportFormatter.format(book, LocalDateTime.of(2026,11,22,0,0)));
        cases.add("ordinary-roundtrip", new Gson().toJsonTree(parsed));
        cases.addProperty("ordinary-roundtrip-equal", original.equals(parsed));
        List<String> collision = List.of("before\n--- Page 99 ---\nafter");
        var marked = new ExtractedBook(BookType.WRITABLE, "fixture", "fixture", collision, BookSource.BOOK_AND_QUILL);
        List<String> split = (List<String>) parse.invoke(null, BookExportFormatter.format(marked, LocalDateTime.of(2026,11,22,0,0)));
        validate.invoke(null, split);
        cases.add("marker-collision-roundtrip", new Gson().toJsonTree(split));
        cases.addProperty("marker-collision-preserved", collision.equals(split));
        require(!collision.equals(split), "expected unescaped page marker finding");
        validate.invoke(null, Collections.nCopies(100, ""));
        validate.invoke(null, List.of("x".repeat(1024)));
        for (var item : Map.of("101-pages", Collections.nCopies(101, ""), "1025-units", List.of("x".repeat(1025))).entrySet()) {
            try { validate.invoke(null, item.getValue()); throw new AssertionError("must reject " + item.getKey()); }
            catch (InvocationTargetException ex) {
                require(ex.getCause() instanceof IllegalArgumentException, "validation failure type");
                cases.addProperty(item.getKey() + "-rejected", true);
            }
        }
        RESULTS.add("book-extractor", cases);
    }

    private static class Reader extends ReadOnlyBookArrowsMixin {
        int count;
        Reader(int count) { this.count = count; }
        protected int getNumPages() { return count; }
        protected void updateButtonVisibility() {}
    }

    private static void bookerCases() throws Exception {
        Method back = ReadOnlyBookArrowsMixin.class.getDeclaredMethod("onGoToPreviousPage", CallbackInfo.class);
        back.setAccessible(true);
        Field page = ReadOnlyBookArrowsMixin.class.getDeclaredField("currentPage");
        page.setAccessible(true);
        Reader reader = new Reader(5);
        back.invoke(reader, new CallbackInfo());
        require(page.getInt(reader) == 4, "ordinary reader wrap");
        JsonObject cases = new JsonObject();
        cases.addProperty("five-page-reader-back-from-first-index", page.getInt(reader));
        try { back.invoke(new Reader(0), new CallbackInfo()); throw new AssertionError("zero-page finding disappeared"); }
        catch (InvocationTargetException ex) {
            require(ex.getCause() instanceof ArithmeticException, "zero-page failure type");
            cases.addProperty("zero-page-reader-exception", ex.getCause().getClass().getSimpleName());
        }
        RESULTS.add("booker", cases);
    }

    public static void main(String[] args) throws Exception {
        pasteCases();
        extractorCases();
        bookerCases();
        System.out.println(new GsonBuilder().disableHtmlEscaping().setPrettyPrinting().create().toJson(RESULTS));
    }
}
