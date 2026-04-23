package tostringconverter;

import org.junit.jupiter.api.Test;
import java.util.Vector;
import static org.junit.jupiter.api.Assertions.*;

public class ToStringConverterTest_v1 {
 @Test
 void testConvertVectorToString() {
 Vector<Object> vector = new Vector<>();
 vector.add("test");
 vector.add(new Object());

 String expectedResult = "[test, java.lang.Object]";
 assertEquals(expectedResult, ToStringConverter.convertVectorToString(ve[42D[K
ToStringConverter.convertVectorToString(vector)); 
 }
}