package org.templateit;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class RegionTest {
 @Test
 void testContainsReference() {
 Reference start = new Reference(0, 0);
 Reference end = new Reference(5, 5);
 Region region = new Region(start, end);
 Reference reference = new Reference(3, 3);
 
 assertTrue(region.contains(reference));
 }

 @Test
 void testContainsRegion() {
 Reference start1 = new Reference(0, 0);
 Reference end1 = new Reference(5, 5);
 Region region1 = new Region(start1, end1);
 
 Reference start2 = new Reference(1, 1);
 Reference end2 = new Reference(3, 3);
 Region region2 = new Region(start2, end2);
 
 assertTrue(region1.contains(region2));
 }

 @Test
 void testDefaultConstructor() {
 Region region = new Region();
 
 assertNull(region.start());
 assertNull(region.end());
 }

 @Test
 void testParameterizedConstructorAndGetters() {
 Reference start = new Reference(1, 2);
 Reference end = new Reference(3, 4);
 Region region = new Region(start, end);
 
 assertEquals(start, region.start());
 assertEquals(end, region.end());
 }

 @Test
 void testSetStartReference() {
 Region region = new Region();
 Reference start = new Reference(1, 2);
 region.setStartReference(start);
 
 assertEquals(start, region.start());
 }

 // New tests for the surviving mutants
 @Test
 void testSetEndReference() {
 Region region = new Region();
 Reference end = new Reference(1, 2);
 region.setEndReference(end);
 
 assertEquals(end, region.end());
 }

 @Test
 void testContainsRegionWithDifferentStartAndEnd() {
 // This is a different start and end to the previous case
 Reference start = new Reference(10, 10);
 Reference end = new Reference(20, 20);
 Region region = new Region(start, end);
 
 // But we still check a reference that should be within this new range
 Reference reference = new Reference(15, 15);
 
 assertTrue(region.contains(reference));
 }
}