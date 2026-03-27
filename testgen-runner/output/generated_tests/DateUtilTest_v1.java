package dateutil;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;
import org.junit.jupiter.api.Test;

public class DateUtilTest_v1 {
 private static final long ONE_DAY = 24 * 60 * 60 * 1000;
 
 @Test
 public void testSetAndRestoreDate() {
 // Save the original system time
 Date originalSystemTime = new Date();
 
 // Set a fixed date and verify getCurrentDate() returns this date
 DateUtil.setCurrentDate(new Date(123, 5, 7));
 assertEquals("Wed Jun 07 00:00:00 PDT 1973", DateUtil.getCurrentDate().toString());
 
 // Restore the original system time and verify getCurrentDate() returns this date
 DateUtil.restoreDate();
 assertTrue(DateUtil.getCurrentDate().after(originalSystemTime));
 }
 
 @Test
 public void testElapsedTimeAsString() {
 // Test with 1 day, 1 hour, 1 minute and 1 second
 assertEquals("P1D", DateUtil.getElapsedTimeAsString(ONE_DAY));
 }
}