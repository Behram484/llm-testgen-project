package com.pmdesigns.jvc.tools;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Base64CoderTest_v1 {
 @Test
 public void testEncodeString() {
 String input = "Hello, World!";
 assertEquals(Base64Coder.encodeString(input), "SGVsbG8sIFdvcmxkIQ==");
 }

 @Test
 public void testDecodeString() {
 String encoded = "SGVsbG8sIFdvcmxkIQ==";
 assertEquals(Base64Coder.decodeString(encoded), "Hello, World!");
 
 // Test decoding an invalid string throws exception
 assertThrows(IllegalArgumentException.class, () -> Base64Coder.decodeSt[20D[K
Base64Coder.decodeString("invalid_base64"));
 }
}