package org;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RegionTest {
 private Reference start = new Reference(0, 0);
 private Reference end = new Reference(2, 2);
 private Region region = new Region(start, end);
 
 @Test
 void testRegion() {
 assertEquals(start, region.start());
 assertEquals(end, region.end());
 
 assertTrue(region.contains(new Reference(0, 0)));
 assertFalse(region.contains(new Reference(-1, -1)));
 
 Region subRegion = new Region(new Reference(1, 1), end);
 assertTrue(region.contains(subRegion));
 }
 
 @Test
 void testReference() {
 assertEquals(0, start.row());
 assertEquals(0, start.column());
 
 assertEquals("0,0", start.toString());
 
 Reference ref = new Reference(1, 1);
 assertTrue(region.contains(ref));
 }
}