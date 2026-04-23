package org;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ReferenceTest_v1 {
 @Test
 void testRowAndColumn() {
 Reference reference = new Reference(5, 3);
 
 assertEquals(5, reference.row(), "Should return the row value");
 assertEquals(3, reference.column(), "Should return the column value");
 }
 
 @Test
 void testHashCode() {
 Reference ref1 = new Reference(5, 3);
 Reference ref2 = new Reference(5, 3);
 
 assertEquals(ref1.hashCode(), ref2.hashCode(), "Should return the same h[1D[K
hashcode for equal objects");
 }
 
 @Test
 void testToString() {
 Reference reference = new Reference(5, 3);
 
 assertEquals("5,3", reference.toString(), "Should return a string repres[6D[K
representation of the object");
 }
}