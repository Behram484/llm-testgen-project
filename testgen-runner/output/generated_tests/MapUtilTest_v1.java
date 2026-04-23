package maputil;

import org.junit.jupiter.api.Test;
import java.util.HashMap;
import static org.junit.jupiter.api.Assertions.*;

public class MapUtilTest_v1 {
 @Test
 public void testBuildStringToIntMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 HashMap<String, String> expectedResult = new HashMap<>();
 expectedResult.put("key1", "value1");
 expectedResult.put("key2", "value2");
 
 assertEquals(expectedResult, MapUtil.buildStringToIntMap(spec));
 }

 @Test
 public void testBuildMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 HashMap<String, String> expectedResult = new HashMap<>();
 expectedResult.put("key1", "value1");
 expectedResult.put("key2", "value2");
 
 assertEquals(expectedResult, MapUtil.buildMap(spec));
 }
 
 @Test
 public void testBuildReversedMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 HashMap<String, String> expectedResult = new HashMap<>();
 expectedResult.put("value1", "key1");
 expectedResult.put("value2", "key2");
 
 assertEquals(expectedResult, MapUtil.buildReversedMap(spec));
 }
}