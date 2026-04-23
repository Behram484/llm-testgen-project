package base32cut;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class Base32Test_v1 {
 @Test
 void testDecode() {
 String encodedString = "BVQXZ";
 byte[] expectedOutput = new byte[]{(byte)0xA4, (byte)0xE9};

 assertArrayEquals(expectedOutput, Base32.decode(encodedString)); 

 // Test empty input
 encodedString = "";
 assertArrayEquals(new byte[0], Base32.decode(encodedString)); 
 }

 @Test
 void testEncode() {
 byte[] input = new byte[]{(byte)0xA4, (byte)0xE9};

 assertEquals(UTUQ, Base32.encode(input)); 

 // Test empty input
 input = new byte[0];
 assertEquals("", Base32.encode(input)); 
 }
}