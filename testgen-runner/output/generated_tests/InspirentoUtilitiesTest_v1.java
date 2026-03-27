package inspirentoutilities;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InspirentoUtilitiesTest {

 @Test
 public void testEscapeText() {
 String input = "Hello & World!";
 assertEquals("Hello &amp; World!", InspirentoUtilities.escapeText(input));
 
 input = "<script>alert('XSS');</script>";
 assertEquals("&lt;script&gt;alert(&apos;XSS&apos;);&lt;/script&gt;", InspirentoUtilities.escapeText(input));
 }
 
 @Test
 public void testTokenize() {
 String input = "file edit view";
 assertArrayEquals(new String[]{"file", "edit", "view"}, InspirentoUtilities.tokenize(input));
 
 String delim = "-";
 assertArrayEquals(new String[]{"file", "edit", "view"}, InspirentoUtilities.tokenize(input, delim));
 }
 
 @Test
 public void testStringReplaceAll() {
 StringBuffer source = new StringBuffer("Hello & World!");
 assertEquals(source, InspirentoUtilities.stringReplaceAll(source,'&',"&amp;"));
 
 source = new StringBuffer("<script>alert('XSS');</script>");
 assertEquals(source, InspirentoUtilities.stringReplaceAll(source,'&',"&amp;"));
 }
}