package org.heal.util;

import static org.junit.jupiter.api.Assertions.*;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.junit.jupiter.api.Test;

class DateToolsTest_v1 {
 @Test
 void testFormatDefault() throws ParseException{
 String expected = "2022-12-31";
 SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
 Date date = sdf.parse(expected);
 assertEquals(expected, DateTools.format(date)); 
 }

 @Test
 void testFormatCustom() {
 String expected = "23:59:00";
 SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");
 try {
 Date date = sdf.parse(expected);
 assertEquals(expected, DateTools.format(date, "HH:mm:ss")); 
 } catch (ParseException e) {
 fail("Error parsing time: " + expected);
 }
 }

 @Test
 void testFormatCustom_wrongDate() {
 String invalidTimeString = "25:00:00";
 assertThrows(IllegalArgumentException.class, () -> DateTools.parse(inva[20D[K
DateTools.parse(invalidTimeString, "HH:mm:ss")); 
 }

 @Test
 void testParseValid() {
 String validDateString = "2022-12-31";
 assertTrue(DateTools.isValidDate(validDateString)); 
 }

 @Test
 void testParseInvalid() {
 String invalidDateString = "31-12-2022";
 assertFalse(DateTools.isValidDate(invalidDateString, "dd-MM-yyyy"));
 }
}