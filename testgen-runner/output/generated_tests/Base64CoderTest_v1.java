package base64coder;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class Base64CoderTest_v1 {
 private Base64Coder base64Coder = new Base64Coder(); // Create an instance of Base64Coder for each test

 @Test
 public void testEncodeStringNormalCase() {
 String encoded = base64Coder.encodeString("Hello");
 assertEquals("SGVsbG8=", encoded);
 }

 @Test
 public void testDecodeStringNormalCase() {
 byte[] decodedBytes = base64Coder.decodeString("SGVsbG8=");
 String decodedString = new String(decodedBytes);
 assertEquals("Hello", decodedString);
 }

 @Test
 public void testEncodeByteArrayNormalCase() {
 byte[] encodedBytes = base64Coder.encode("Hello".getBytes());
 assertArrayEquals(new char[]{'S', 'G', 'V', 's', 'b', 'G', '8', '='}, new char[]{encodedBytes[0], encodedBytes[1], encodedBytes[2], encodedBytes[3], encodedBytes[4], encodedBytes[5], encodedBytes[6], encodedBytes[7]});
 }

 @Test
 public void testDecodeByteArrayNormalCase() {
 byte[] decodedBytes = base64Coder.decode(new char[]{'S', 'G', 'V', 's', 'b', 'G', '8', '='});
 assertArrayEquals("Hello".getBytes(), decodedBytes);
 }
}