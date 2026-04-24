package net.sourceforge.squirrel_sql.fw.datasetviewer.cellcomponent;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class BinaryDisplayConverterTest_v1 {
 
 @Test
 public void testConvertToString() {
 Byte[] data = new Byte[]{(byte)0xFF, (byte)0xAA};
 
 String expectedResult = "255 170 ";
 String actualResult = BinaryDisplayConverter.convertToString(data, Bina[4D[K
BinaryDisplayConverter.HEX, false);
 Assertions.assertEquals(expectedResult, actualResult);
 }

 @Test
 public void testConvertToBytes() {
 String data = "255 170 ";
 
 Byte[] expectedResult = new Byte[]{(byte)0xFF, (byte)0xAA};
 Byte[] actualResult = BinaryDisplayConverter.convertToBytes(data, Binar[5D[K
BinaryDisplayConverter.HEX, false);
 Assertions.assertArrayEquals(expectedResult, actualResult);
 }
 
 @Test
 public void testNullInputConvertToString() {
 String expectedResult = null;
 String actualResult = BinaryDisplayConverter.convertToString(null, Bina[4D[K
BinaryDisplayConverter.HEX, false);
 
 Assertions.assertEquals(expectedResult, actualResult);
 }
 
 @Test
 public void testNullInputConvertToBytes() {
 Byte[] expectedResult = null; and