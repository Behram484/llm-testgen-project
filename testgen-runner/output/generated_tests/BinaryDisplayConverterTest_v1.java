package binarydisplayconverter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class BinaryDisplayConverterTest_v1 {
 
 @Test
 void convertToString_decimalData() {
 Byte[] data = new Byte[]{Byte.valueOf("12"), Byte.valueOf("34")};
 int base = BinaryDisplayConverter.DECIMAL;
 boolean showAscii = false;

 assertEquals("000012 000034 ", BinaryDisplayConverter.convertToString(data, base, showAscii));
 }
}