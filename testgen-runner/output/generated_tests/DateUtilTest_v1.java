package org.jcvi.jillion.core.util;

import java.util.Date;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class DateUtilTest_v1 {
 @Test
 void testGetCurrentDate() {
 // Given no current date set
 DateUtil.restoreDate();

 // When getting the current date
 Date currentDate = DateUtil.getCurrentDate();

 // Then the returned date is close to now, within a few seconds
 long now = System.currentTimeMillis();
 assertTrue(Math.abs((now - currentDate.getTime()) / 1000) < 5);
 }

 @Test
 void testSetCurrentDate() {
 // Given a specific date to set
 Date specifiedDate = new Date(2023-1900, 8, 5, 14, 30); 

 // When setting the current date to that specific date
 DateUtil.setCurrentDate(specifiedDate);

 // Then getting the current date returns that specified date
 assertEquals(specifiedDate, DateUtil.getCurrentDate());
 }

 @Test
 void testRestoreDate() {
 // Given a specific date is set and we have restored it
 Date specifiedDate = new Date(2023-1900, 8, 5, 14, 30); 
 DateUtil.setCurrentDate(specifiedDate);
 DateUtil.restoreDate();

 // When getting the current date
 Date currentDate = DateUtil.getCurrentDate();

 // Then the returned date is close to now, within a few seconds
 long now = System.currentTimeMillis();
 assertTrue(Math.abs((now - currentDate.getTime()) / 1000) < 5);
 }

 @Test
 void testSetCurrentDateWithNull() {
 // Given a null date is set

 // When setting the current date to that specific date
 // Then an exception should be thrown
 assertThrows(NullPointerException.class, () -> DateUtil.setCurrentDate([24D[K
DateUtil.setCurrentDate(null));
 }
}