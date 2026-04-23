package binarydisplayconverter;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BinaryDisplayConverterTest_v1 {
 private final BinaryDisplayConverter bdc = new BinaryDisplayConverter(); [K
// create instance of the converter to call its methods

 @Test
 void testConvertToStringBinary() {
 Byte[] data = {(byte)0b00000000, (byte)0b11111111, (byte)0b10011010, (b[2D[K
(byte)0b10011010};
 String expectedResult = "00 255 146";
 boolean showAscii = false;

 assertEquals(expectedResult, bdc.convertToString(data, 2, showAscii)); [K
// call method using the instance of converter
 }

 @Test
 void testConvertToBytesBinary() {
 String data = "00 255 146";
 Byte[] expectedResult = {(byte)0b00000000, (byte)0b11111111, (byte)0b10[10D[K
(byte)0b10011... and 7 more ...s. (byte)0b10011010[16D[K
(byte)0b10011010};
 boolean showAscii = false;

 assertArrayEquals(expectedResult, bdc.convertToBytes(data, 2, showAscii[9D[K
showAscii)); // call method using the instance of converter
 }

 @Test
 void testConvertToStringHex() {
 Byte[] data = {(byte)0b10101010, (byte)0b10011010};
 String expectedResult = "aa 9a";
 boolean showAscii = false;

 assertEquals(expectedResult, bdc.convertToString(data, 16, showAscii));[12D[K
showAscii)); // call method using the instance of converter
 }

 @Test
 void testConvertToBytesHex() {
 String data = "aa 9a";
 Byte[] expectedResult = {(byte)0b10101010, (byte)0b10011010};
 boolean showAscii = false;

 assertArrayEquals(expectedResult, bdc.convertToBytes(data, 16, showAsci[8D[K
showAscii)); // call method using the instance of converter
 }
}