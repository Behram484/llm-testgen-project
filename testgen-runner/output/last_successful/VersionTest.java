package version;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class VersionTest {
 @Test
 public void testCompareTo() {
 Version version1 = new Version("1.2.3");
 Version version2 = new Version("1.2.4");
 
 assertEquals(-1, version1.compareTo(version2));
 }

 @Test
 public void testEquals_sameVersions() {
 Version version1 = new Version("1.2.3");
 Version version2 = new Version("1.2.3");
 
 assertTrue(version1.equals(version2));
 }
 
 @Test
 public void testEquals_differentVersions() {
 Version version1 = new Version("1.2.3");
 Version version2 = new Version("1.2.4");
 
 assertFalse(version1.equals(version2));
 }
 
 @Test
 public void testHashCode_sameVersions() {
 Version version1 = new Version("1.2.3");
 Version version2 = new Version("1.2.3");
 
 assertEquals(version1.hashCode(), version2.hashCode());
 }
 
 @Test
 public void testHashCode_differentVersions() {
 Version version1 = new Version("1.2.3");
 Version version2 = new Version("1.2.4");
 
 assertNotEquals(version1.hashCode(), version2.hashCode());
 }
 
 @Test
 public void testToString() {
 Version version1 = new Version("1.2.3");
 
 assertEquals("1.2.3", version1.toString());
 }
}