package org.templateit;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ReferenceTest {
 @Test
 void testReferenceCreation() {
 Reference ref = new Reference(5, 3);
 
 assertEquals(5, ref.row());
 assertEquals(3, ref.column());
 }
 
 @Test
 void testHashCodeAndEquals() {
 Reference ref1 = new Reference(2, 4);
 Reference ref2 = new Reference(2, 4);
 
 assertTrue(ref1.equals(ref2));
 assertEquals(ref1.hashCode(), ref2.hashCode());
 }
 
 @Test
 void testToString() {
 Reference ref = new Reference(7, 9);
 
 assertEquals("7,9", ref.toString());
 }

 @Test
 void testEqualsWithDifferentObjects() {
 Reference ref1 = new Reference(2, 4);
 Object ref2 = new Object();
 
 assertFalse(ref1.equals(ref2));
 }
 
 @Test
 void testHashCodeOnDifferentObjects() {
 Reference ref1 = new Reference(2, 4);
 Object ref2 = new Object();
 
 assertNotEquals(ref1.hashCode(), ref2.hashCode());
 }
}