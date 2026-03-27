package maputil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class MapUtilTest {
 @Test
 public void testBuildStringToIntMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 Map<String, String> map = MapUtil.buildStringToIntMap(spec);
 
 assertEquals("value1", map.get("key1"));
 assertEquals("value2", map.get("key2"));
 }
 
 @Test
 public void testBuildMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 Map<String, String> map = MapUtil.buildMap(spec);
 
 assertEquals("value1", map.get("key1"));
 assertEquals("value2", map.get("key2"));
 }
 
 @Test
 public void testBuildReversedMap() {
 Object[] spec = {"key1", "value1", "key2", "value2"};
 Map<String, String> map = MapUtil.buildReversedMap(spec);
 
 assertEquals("key1", map.get("value1"));
 assertEquals("key2", map.get("value2"));
 }
}