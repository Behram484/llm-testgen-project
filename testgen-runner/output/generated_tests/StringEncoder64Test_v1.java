package osa.ora.server.utils;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.io.ByteArrayOutputStream;
import static org.junit.jupiter.api.Assertions.*;

public class StringEncoder64Test_v1 {
 private StringEncoder64 encoder;
 
 @BeforeEach
 void setup() {
 // Create instance of StringEncoder64 for testing
 encoder = new StringEncoder64();
 }
 
 @Test
 void testEncodeStringUTF8_normalCase() {
 assertEquals("dGVzdA==", encoder.encodeStringUTF8("test"));
 }
 
 @Test
 void testEncodeStringUTF8_nullInput() {
 assertThrows(NullPointerException.class, () -> encoder.encodeStringUTF8[24D[K
encoder.encodeStringUTF8(null));
 }
 
 @Test
 void testDecodeStringUTF8_normalCase() {
 assertEquals("test", new String(encoder.decodeStringUTF8("dGVzdA==")));[46D[K
String(encoder.decodeStringUTF8("dGVzdA==")));
 }
 
 @Test
 void testDecodeStringUTF8_nullInput() {
 assertThrows(NullPointerException.class, () -> encoder.decodeStringUTF8[24D[K
encoder.decodeStringUTF8(null));
 }
}