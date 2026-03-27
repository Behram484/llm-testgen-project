package base64;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Base64;
import org.apache.commons.codec.binary.Base64 as ApacheBase64;
import org.junit.jupiter.api.Test;

public class Base64Test_v1 {
 @Test
 void testAltBase64ToByteArray() {
 String input = "dGVzdA=="; //"test" in base64 encoding with padding
 byte[] expectedOutput = new byte[]{(byte)0x74, (byte)0x65, (byte)0x73, (byte)0x74}; //"test" in bytes
 assertArrayEquals(expectedOutput, Base64.getDecoder().decode(input));
 }

 @Test
 void testBase64ToByteArray() {
 String input = "dGVzdA=="; //"test" in base64 encoding with padding
 byte[] expectedOutput = new byte[]{(byte)0x74, (byte)0x65, (byte)0x73, (byte)0x74}; //"test" in bytes
 assertArrayEquals(expectedOutput, ApacheBase64.decodeBase64(input));
 }

 @Test
 void testByteArrayToAltBase64() {
 byte[] input = new byte[]{(byte)0x74, (byte)0x65, (byte)0x73, (byte)0x74}; //"test" in bytes
 String expectedOutput = "dGVzdA=="; //"test" in base64 encoding with padding
 assertEquals(expectedOutput, new String(Base64.getEncoder().encode(input)));
 }

 @Test
 void testByteArrayToBase64() {
 byte[] input = new byte[]{(byte)0x74, (byte)0x65, (byte)0x73, (byte)0x74}; //"test" in bytes
 String expectedOutput = "dGVzdA=="; //"test" in base64 encoding with padding
 assertEquals(expectedOutput, ApacheBase64.encodeBase64String(input));
 }
}