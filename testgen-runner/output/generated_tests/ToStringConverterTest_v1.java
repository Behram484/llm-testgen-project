package de.paragon.explorer.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Vector;

public class ToStringConverterTest_v1 {
 @Test
 public void testConvertVectorToString() {
 Vector<Object> vector = new Vector<>();
 vector.add("test");
 vector.add(null);
 String expectedResult = "[test, null]";
 assertEquals(expectedResult, ToStringConverter.convertVectorToStrin[38D[K
ToStringConverter.convertVectorToString(vector));
 }

 @Test
 public void testConvertVectorToStringWithCircularReference() {
 Vector<Object> vector1 = new Vector<>();
 Vector<Object> vector2 = new Vector<>();
 vector1.add(vector2);
 vector2.add(vector1);
 assertThrows(StackOverflowError.class, () -> ToStringConverter.conv[22D[K
ToStringConverter.convertVectorToString(vector1));
 }
}