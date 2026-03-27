package datetools;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;
import java.text.SimpleDateFormat;

public class DateToolsTest {
 @Test
 public void testIsValidDateWithInvalidDateString() {
 String dateString = "2022-13-31"; // invalid month
 assertFalse(DateTools.isValidDate(dateString));
 }

 @Test
 public void testParseWithInvalidDateStringAndFormat() {
 String dateString = "2022-13-31"; // invalid month
 Date expected = null;
 assertEquals(expected, DateTools.parse(dateString, DateTools.DEFAULT_DATE_FORMAT));
 }

 @Test
 public void testIsValidDateWithInvalidLeapYear() {
 String dateString = "2019-02-30"; // February has only 28 days in a common year
 assertFalse(DateTools.isValidDate(dateString));
 }

 @Test
 public void testParseWithInvalidLeapYear() {
 String dateString = "2019-02-30"; // February has only 28 days in a common year
 Date expected = null;
 assertEquals(expected, DateTools.parse(dateString));
 }
}