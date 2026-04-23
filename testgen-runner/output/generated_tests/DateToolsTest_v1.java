package datetools;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;

public class DateToolsTest_v1 {
 @Test
 void testFormatWithNullInput() {
 assertNull(DateTools.format(null));
 }

 @Test
 void testFormatWithDefaultFormat() {
 Date date = new Date();
 String expected = "2022-12-31"; // Use the current year, month and day [K
for determinism
 assertEquals(expected, DateTools.format(date));
 }

 @Test
 void testFormatWithSpecificFormat() {
 Date date = new Date();
 String format = "yyyy-MM-dd HH:mm:ss"; // Use the current year month an[2D[K
and day for determinism
 assertEquals("2022-12-31 00:00:00", DateTools.format(date, format)); 
 }

 @Test
 void testParseWithNullInput() {
 assertNull(DateTools.parse(null));
 }

 @Test
 void testParseWithDefaultFormat() {
 String dateString = "2022-12-31"; // Use the current year month and day[3D[K
day for determinism
 Date expected = new Date();
 assertEquals(expected, DateTools.parse(dateString));
 }

 @Test
 void testParseWithSpecificFormat() {
 String dateString = "2022-12-31 12:34:56"; // Use the current year mont[4D[K
month and day for determinism
 Date expected = new Date();
 assertEquals(expected, DateTools.parse(dateString, "yyyy-MM-dd HH:mmt"));
 }

 @Test
 void testIsValidDateWithNullInput() {
 assertThrows(java.text.ParseException.class, () -> DateTools.isValidDat[20D[K
DateTools.isValidDate(null));
 }

 @Test
 void testIsValidDateWithDefaultFormat() {
 String dateString = "2022-12-31"; // Use the current year month and day[3D[K
day for determinism
 assertTrue(DateTools.isValidDate(dateString));
 }

 @Test
 void testIsValidDateWithSpecificFormat() {
 String dateString = "2022-12-31 12:34:56"; // Use the current year mont[4D[K
month and day for determinism
 assertTrue(DateTools.isValidDate(dateString, "yyyy-MM-dd HH:mm:ss"));
 }
}