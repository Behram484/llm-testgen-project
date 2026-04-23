package htmlencoder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HtmlEncoderTest_v1 {
 private final HtmlEncoder encoder = new HtmlEncoder(); // Create an in[2D[K
instance of the encoder for testing

 @Test
 void testEncodeTokenWithChar() {
 assertEquals("&lt;", HtmlEncoder.encodeToken('<'));
 assertEquals("&gt;", HtmlEncoder.encodeToken('>'));
 assertEquals("<br>" + System.lineSeparator(), HtmlEncoder.encodeTok[21D[K
HtmlEncoder.encodeToken("\n"));
 }

 @Test
 void testEncodeTokenWithString() {
 assertEquals("&lt;", HtmlEncoder.encodeToken("<"));
 assertEquals("&gt;", HtmlEncoder.encodeToken(">"));
 assertEquals("<br>" + System.lineSeparator(), HtmlEncoder.encodeTok[21D[K
HtmlEncoder.encodeToken("\n"));
 }

 @Test
 void testEncodeString() {
 String input = "< >\n";
 String expectedOutput = "&lt; &gt;" + "<br>" + System.lineSeparator[20D[K
System.lineSeparator();
 assertEquals(expectedOutput, HtmlEncoder.encodeString(input));
 }
}