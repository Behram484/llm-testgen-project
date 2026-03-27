package org;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class ReferenceTest {

 @Test
 void testRow() {
 Reference reference = new Reference(5, 3);
 assertEquals(5, reference.row());
 }

 @Test
 void testColumn() {
 Reference reference = new Reference(5, 3);
 assertEquals(3, reference.column());
 }

 @Test
 void testHashCodeAndEquals() {
 Reference reference1 = new Reference(5, 3);
 Reference reference2 = new Reference(5, 3);
 assertTrue(reference1.equals(reference2) && reference2.equals(reference1));
 assertEquals(reference1.hashCode(), reference2.hashCode());
 
 // Test different objects with the same values
 Reference reference3 = new Reference(5, 3);
 assertNotEquals(0, reference1.hashCode() - reference3.hashCode());
 assertFalse(reference1.equals(new Object()));
 }

 @Test
 void testToString() {
 Reference reference = new Reference(5, 3);
 assertEquals("5,3", reference.toString());
 
 // Test with different values
 Reference reference2 = new Reference(10, 6);
 assertNotEquals("5,3", reference2.toString());
 }

 @Test
 void testRegionContainsReference(){
 Region region = new Region(new Reference(1, 1), new Reference(10, 10));
 assertTrue(region.contains(new Reference(5,5)));
 assertFalse(region.contains(new Reference(11,5)));
 
 // Test with different values
 assertFalse(region.contains(new Reference(-1,-1)));
 }

 @Test
 void testRegionContainsRegion(){
 Region region1 = new Region(new Reference(1, 1), new Reference(10, 10));
 Region region2 = new Region(new Reference(5, 5), new Reference(8, 8));
 assertTrue(region1.contains(region2));
 
 // Test with different values
 Region region3 = new Region(new Reference(6, 6), new Reference(9, 9));
 assertFalse(region1.contains(region3));
 }
 
 @Test
 void testSetStartReference() {
 Reference reference = new Reference(5, 3);
 Reference startReference = new Reference(2, 1);
 Region region = new Region();
 region.setStartReference(startReference);
 
 // Start references are equal
 assertEquals(region.start(), startReference);
 }
 
 @Test
 void testSetEndReference() {
 Reference endReference = new Reference(8, 9);
 Region region = new Region();
 region.setEndReference(endReference);
 
 // End references are equal
 assertEquals(region.end(), endReference);
 }
}