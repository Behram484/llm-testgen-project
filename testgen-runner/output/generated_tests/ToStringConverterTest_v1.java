package tostringconverter;

import java.util.Vector;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class ToStringConverterTest_v1 {
 @Test
 void testConvertVectorToString() {
 Vector<Object> vector = new Vector<>();
 vector.add("test");
 vector.add(new Object());
 
 String expectedResult = "[test, java.lang.Object@d62fe5b]"; // Hashcode of the object is different for every run
 String actualResult = ToStringConverter.convertVectorToString(vector);

 assertEquals(expectedResult, actualResult);
 }
}