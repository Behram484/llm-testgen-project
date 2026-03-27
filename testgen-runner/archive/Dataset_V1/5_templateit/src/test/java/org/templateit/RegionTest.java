package org.templateit;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class RegionTest {

 @Test
 void testContainsRegion() {
 Region region1 = new Region(new Reference(1, 1), new Reference(3, 3));
 Region region2 = new Region(new Reference(1, 1), new Reference(4, 4));
 assertTrue(region1.contains(region2));
 }

 @Test
 void testContainsReference() {
 Region region = new Region(new Reference(1, 1), new Reference(3, 3));
 assertTrue(region.contains(new Reference(2, 2)));
 }

 @Test
 void testSetStartReference() {
 Region region = new Region(new Reference(1, 1), new Reference(3, 3));
 region.setStartReference(new Reference(2, 2));
 assertEquals(new Reference(2, 2), region.start());
 }

 @Test
 void testSetEndReference() {
 Region region = new Region(new Reference(1, 1), new Reference(3, 3));
 region.setEndReference(new Reference(2, 2));
 assertEquals(new Reference(2, 2), region.end());
 }

 @Test
 void testToString() {
 Region region = new Region(new Reference(1, 1), new Reference(3, 3));
 assertEquals("Reference{row=1, column=1}, Reference{row=3, column=3}", region.toString());
 }
}