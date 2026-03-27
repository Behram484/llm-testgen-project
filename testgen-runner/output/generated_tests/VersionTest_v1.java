package version;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class VersionTest_v1 {
 @Test
 void testEquals() {
 Version v1 = new Version("1.2.3");
 Version v2 = new Version("1.2.3");
 assertTrue(v1.equals(v2));
 assertTrue(v2.equals(v1));
 }
 
 @Test
 void testNotEquals() {
 Version v1 = new Version("1.2.4");
 Version v2 = new Version("1.2.3");
 assertFalse(v1.equals(v2));
 assertFalse(v2.equals(v1));
 }
 
 @Test
 void testCompareTo() {
 Version v1 = new Version("1.2.3");
 Version v2 = new Version("1.2.4");
 assertTrue(v1.compareTo(v2) < 0);
 assertTrue(v2.compareTo(v1) > 0);
 }
 
 @Test
 void testHashCode() {
 Version v1 = new Version("1.2.3");
 assertEquals(v1.hashCode(), 6); // hashcode for '1' + '2' + '3' = 6
 }
 
 @Test
 void testToString() {
 Version v1 = new Version("1.2.3");
 assertEquals(v1.toString(), "1.2.3");
 }
}