package net.sourceforge.schemaspy.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class VersionTest {
 @Test
 void testVersionCompareTo() {
 Version v1 = new Version("1.0");
 assertEquals(-1, v1.compareTo(new Version("2.0")));
 assertEquals(0, v1.compareTo(new Version("1.0")));
 assertEquals(1, v1.compareTo(new Version("0.9")));
 }

 @Test
 void testVersionHashCode() {
 Version v1 = new Version("1.0");
 assertEquals(v1.hashCode(), new Version("1.0").hashCode());
 }

 @Test
 void testVersionToString() {
 Version v1 = new Version("1.0");
 assertEquals("1.0", v1.toString());
 }

 @Test
 void testVersionEquals() {
 Version v1 = new Version("1.0");
 assertTrue(v1.equals(new Version("1.0")));
 assertFalse(v1.equals(new Version("2.0")));
 
 Exception exception = assertThrows(NullPointerException.class, () -> v1[2D[K
v1.equals(null));
 assertEquals("Comparison with null not allowed", exception.getMessage()[22D[K
exception.getMessage());
 }
}