package base32cut;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Base32Test_v1 {
 @Test
 void testDecode() {
 String input = "JBSWY3DPK5XXE3DE";
 byte[] expectedOutput = "Hello, World!".getBytes();

 assertArrayEquals(expectedOutput, Base32.decode(input));
 }

 @Test
 void testEncode() {
 byte[] input = "Hello, World!".getBytes();
 String expectedOutput = "JBSWY3DPK5XXE3DE";

 assertEquals(expectedOutput, Base32.encode(input));
 }
}