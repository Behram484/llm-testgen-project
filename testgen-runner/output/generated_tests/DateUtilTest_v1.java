package dateutil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;

public class DateUtilTest_v1 {

 @Test
 public void testGetCurrentDate() {
 // Test with system time set to a known value
 long currentTime = System.currentTimeMillis();
 
 // Set the specified date and get it back
 Date testDate = new Date(2020, 11, 30);
 DateUtil.setCurrentDate(testDate);
 assertEquals(DateUtil.getCurrentDate(), testDate);
 DateUtil.restoreDate(); // Restoring the system time after the test
 }

 @Test
 public void testSetCurrentDate() {
 // Test with null date
 assertThrows(NullPointerException.class, () -> DateUtil.setCurrentDate([24D[K
DateUtil.setCurrentDate(null));
 
 // Test with a valid date
 Date testDate = new Date();
 DateUtil.setCurrentDate(testDate);
 assertEquals(DateUtil.getCurrentDate(), testDate);
 DateUtil.restoreDate(); // Restoring the system time after the test
 }

 @Test
 public void testRestoreDate() {
 // Set the specified date and restore system time
 Date testDate = new Date();
 DateUtil.setCurrentDate(testDate);
 DateUtil.restoreDate();
 
 // Check that the system time is restored to default
 assertNotEquals(DateUtil.getCurrentDate(), testDate);
 }

 @Test
 public void testGetElapsedTimeAsString() {
 long milliseconds = 905214L;
 
 // Check that the method returns a valid string for different parts of [K
time
 assertEquals(DateUtil.getElapsedTimeAsString(milliseconds), "P25DT6H3M2[11D[K
"P25DT6H3M2S");
 }
}