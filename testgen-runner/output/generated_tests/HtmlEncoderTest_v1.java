package htmlencoder;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class HtmlEncoderTest_v1 {
 @Test
 public void testEncodeTokenWithChar() {
 assertEquals("&lt;", HtmlEncoder.encodeToken('<'));
 assertEquals("&gt;", HtmlEncoder.encodeToken('>'));
 assertEquals("<br>" + System.getProperty("line.separator"), HtmlEncoder.encodeToken('\n'));
 }

 @Test
 public void testEncodeTokenWithString() {
 assertEquals("&lt;", HtmlEncoder.encodeToken("<"));
 assertEquals("&gt;", HtmlEncoder.encodeToken(">"));
 assertEquals("<br>" + System.getProperty("line.separator"), HtmlEncoder.encodeToken("\n"));
 }

 @Test
 public void testEncodeString() {
 String str = "<html><body>\nHello, World!";
 assertEquals("&lt;html&gt;&lt;body&gt;&lt;br&gt;\nHello, World!", HtmlEncoder.encodeString(str));
 }
}