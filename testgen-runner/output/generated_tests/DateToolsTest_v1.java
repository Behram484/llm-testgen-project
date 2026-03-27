package datetools;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;
import java.text.SimpleDateFormat;

public class DateToolsTest_v1 {
 @Test
 public void testFormatWithDefaultDateFormat() throws Exception {
 SimpleDateFormat formatter = new SimpleDateFormat(DateTools.DEFAULT_DATE_FORMAT);
 Date date = formatter.parse("2022-12-31"); // assuming current year is 2022, month is December and day is 31
 
 String expected = "2022-12-31"; 
 assertEquals(expected, DateTools.format(date));
 }

 @Test
 public void testFormatWithLongDateFormat() throws Exception {
 SimpleDateFormat formatter = new SimpleDateFormat(DateTools.LONG_DATE_FORMAT);
 Date date = formatter.parse("2022-12-31 00:00:00"); // assuming current time is midnight
 
 String expected = "2022-12-31 00:00:00"; 
 assertEquals(expected, DateTools.format(date, DateTools.LONG_DATE_FORMAT));
 }

 @Test
 public void testIsValidDateWithValidDateString() {
 String dateString = "2022-12-31";
 assertTrue(DateTools.isValidDate(dateString));
 }
 
 @Test
 public void testParseWithValidDateString() {
 String dateString = "2022-12-31";
 // assuming current year is 2022, month is December and day is 31
 Date expected = new Date(122, 11, 31);
 assertEquals(expected, DateTools.parse(dateString));
 }
 
 @Test
 public void testIsValidDateWithValidDateStringAndFormat() {
 String dateString = "2022-12-31 00:00:00";
 assertTrue(DateTools.isValidDate(dateString, DateTools.LONG_DATE_FORMAT));
 }
 
 @Test
 public void testParseWithValidDateStringAndFormat() {
 String dateString = "2022-12-31";
 // assuming current year is 2022, month is December and day is 31
 Date expected = new Date(122, 11, 31);
 assertEquals(null, DateTools.parse(dateString, DateTools.LONG_DATE_FORMAT));
 }
}