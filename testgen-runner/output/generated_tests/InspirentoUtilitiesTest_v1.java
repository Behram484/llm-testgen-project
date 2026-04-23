package inspirentoutilities;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InspirentoUtilitiesTest_v1 {
 @Test
 void testTokenizeWithDefaultDelimiter() {
 String[] expected = {"Hello", "World"};
 assertArrayEquals(expected, InspirentoUtilities.tokenize("Hello World")[7D[K
World"));
 }

 @Test
 void testTokenizeWithCustomDelimiter() {
 String[] expected = {"Hello", "World"};
 assertArrayEquals(expected, InspirentoUtilities.tokenize("Hello|World",[43D[K
InspirentoUtilities.tokenize("Hello|World", "|"));
 }

 @Test
 void testEscapeTextWithSpecialCharacters() {
 String input = "Hello & < > \" '";
 String expected = "Hello &amp; &lt; &gt; &quot; &apos;";
 assertEquals(expected, InspirentoUtilities.escapeText(input));
 }
}