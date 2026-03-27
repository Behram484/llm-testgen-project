package org;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class RegionTest {
 
 @Test
 void testDefaultConstructor() {
 Region region = new Region();
 assertNull(region.start());
 assertNull(region.end());
 }
 
 @Test
 void testNonDefaultConstructorWithTwoReferences() {
 Reference start = new Reference(1, 2);
 Reference end = new Reference(3, 4);
 Region region = new Region(start, end);
 
 assertEquals(start, region.start());
 assertEquals(end, region.end());
 }
 
 @Test
 void testSetStartReference() {
 Reference start = new Reference(1, 2);
 Region region = new Region();
 region.setStartReference(start);
 
 assertEquals(start, region.start());
 }

 @Test
 void testSetEndReference() {
 Reference end = new Reference(3, 4);
 Region region = new Region();
 region.setEndReference(end);
 
 assertEquals(end, region.end());
 }
 
 @Test
 void testContainsRegion() {
 Region parent = new Region(new Reference(1, 2), new Reference(3, 4));
 Region child = new Region(new Reference(1, 2), new Reference(2, 3));
 
 assertTrue(parent.contains(child));
 }
 
 @Test
 void testContainsReference() {
 Region region = new Region(new Reference(1, 2), new Reference(3, 4));
 Reference reference = new Reference(2, 3);
 
 assertTrue(region.contains(reference));
 }
 
 @Test
 void testContainsReferenceOutside() {
 Region region = new Region(new Reference(1, 2), new Reference(3, 4));
 Reference reference = new Reference(5, 6);
 
 assertFalse(region.contains(reference));
 }
 
 @Test
 void testContainsRegionOutside() {
 Region parent = new Region(new Reference(1, 2), new Reference(3, 4));
 Region child = new Region(new Reference(5, 6), new Reference(7, 8));
 
 assertFalse(parent.contains(child));
 }
 
}