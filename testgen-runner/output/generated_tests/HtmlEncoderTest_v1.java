package net.sourceforge.schemaspy.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HtmlEncoderTest_v1 {
 @Test
 public void testEncodeTokenChar() {
 assertEquals("&lt;", HtmlEncoder.encodeToken('<'));
 assertEquals("&gt;", HtmlEncoder.encodeToken('>'));
 assertEquals("<br>" + System.lineSeparator(), HtmlEncoder.encodeToken("[25D[K
HtmlEncoder.encodeToken("\n"));
 }

 @Test
 public void testEncodeTokenString() {
 assertEquals("&lt;", HtmlEncoder.encodeToken("<"));
 assertEquals("&gt;", HtmlEncoder.encodeToken(">"));
 assertEquals("<br>" + System.lineSeparator(), HtmlEncoder.encodeToken("[25D[K
HtmlEncoder.encodeToken("\n"));
 }

 @Test
 public void testEncodeString() {
 assertEquals("&lt;&gt;", HtmlEncoder.encodeString("<>"));
 assertThrows(NullPointerException.class, () -> HtmlEncoder.encodeString[24D[K
HtmlEncoder.encodeString(null));
 }
}