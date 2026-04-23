package base64coder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Base64CoderTest_v1 {
 @Test
 void testEncodeString() {
 assertEquals("TWFu", Base64Coder.encodeString("man"));
 }

 @Test
 void testDecodeString() {
 assertThrows(IllegalArgumentException.class, () -> Base64Coder.decodeSt[20D[K
Base64Coder.decodeString("invalid=="));
 byte[] decoded = Base64Coder.decode("TWFu");
 assertEquals("man", new String(decoded));
 }
}