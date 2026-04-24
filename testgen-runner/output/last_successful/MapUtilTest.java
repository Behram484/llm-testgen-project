package com.lts.util;

import org.junit.jupiter.api.Test;
import java.util.HashMap;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

public class MapUtilTest {
 @Test
 void testBuildStringToIntMap() {
 Object[] spec = {"one", 1, "two", 2, "three", 3};
 Map<String, Integer> expectedMap = new HashMap<>();
 expectedMap.put("one", 1);
 expectedMap.put("two", 2);
 expectedMap.put("three", 3);

 Map<String, Integer> resultMap = MapUtil.buildStringToIntMap(spec);

 assertEquals(expectedMap, resultMap);
 }
 
 @Test
 void testBuildMap() {
 Object[] spec1D = {"one", 1, "two", 2, "three", 3};
 Map<Object, Object> expectedMap1D = new HashMap<>();
 expectedMap1D.put("one", 1);
 expectedMap1D.put("two", 2);
 expectedMap1D.put("three", 3);

 Map<Object, Object> resultMap1D = MapUtil.buildMap(spec1D);

 assertEquals(expectedMap1D, resultMap1D);
 
 Object[][] spec2D = {{"one", 1}, {"two", 2}, {"three", 3}};
 Map<Object, Object> expectedMap2D = new HashMap<>();
 expectedMap2D.put("one", 1);
 expectedMap2D.put("two", 2);
 expectedMap2D.put("three", 3);
 
 Map<Object, Object> resultMap2D = MapUtil.buildMap(spec2D);

 assertEquals(expectedMap2D, resultMap2D);
 }
 
 @Test
 void testBuildReversedMap() {
 Object[] spec = {"one", 1, "two", 2, "three", 3};
 Map<Integer, String> expectedMap = new HashMap<>();
 expectedMap.put(1, "one");
 expectedMap.put(2, "two");
 expectedMap.put(3, "three");

 Map<Integer, String> resultMap = MapUtil.buildReversedMap(spec);

 assertEquals(expectedMap, resultMap);
 }
}