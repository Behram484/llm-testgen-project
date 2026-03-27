package stringencoder64;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StringEncoder64Test_v1 {
 @Test
 public void testEncodeAndDecodeByteArray() {
 byte[] originalBytes = "Hello, World!".getBytes();
 byte[] encodedBytes = new StringEncoder64().encode(originalBytes).getBytes();
 assertArrayEquals(originalBytes, StringEncoder64.decode(new String(encodedBytes)));
 }

 @Test
 public void testEncodeAndDecodePartOfByteArray() {
 byte[] originalBytes = "Hello, World!".getBytes();
 int start = 0;
 int len = originalBytes.length;
 String encodedString = new String(originalBytes);
 assertArrayEquals(originalBytes, StringEncoder64.decode(new StringEncoder64().encode(originalBytes, start, len)));
 }

 @Test
 void testEncodeStringUTF8AndDecodeStringUTF8() {
 String original = "Hello, World!";
 String encoded = StringEncoder64.encodeStringUTF8(original);
 assertEquals(original, StringEncoder64.decodeStringUTF8(encoded));
 }
}