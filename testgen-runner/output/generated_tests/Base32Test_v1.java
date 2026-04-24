package org.gudy.azureus2.core3.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Base32Test_v1 {
 @Test
 void testEncodeDecode() {
 // Normal case: simple byte array
 byte[] bytes = new byte[]{(byte)0x48, (byte)0x65, (byte)0x6c, (byte)0x6[9D[K
(byte)0x6c, (byte)0x6f};
 String encoded = Base32.encode(bytes);
 byte[] decoded = Base32.decode(encoded);
 assertEquals("HELLO", new String(decoded));
 
 // Empty case: empty byte array
 bytes = new byte[]{};
 encoded = Base32.encode(bytes);
 assertTrue(encoded.isEmpty());
 }
}