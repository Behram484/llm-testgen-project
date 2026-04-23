package commandline;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CommandLineTest_v1 {
 @Test
 public void testExists() {
 // create an instance of the tested class
 CommandLine cmd = new CommandLine(new String[]{"-a", "b"});
 
 assertTrue(cmd.exists("a"));
 assertFalse(cmd.exists("c"));
 }
 
 @Test
 public void testIsSwitch() {
 // create an instance of the tested class
 CommandLine cmd = new CommandLine(new String[]{"-a", "b"});
 
 assertTrue(cmd.isSwitch("a"));
 assertFalse(cmd.isSwitch("b"));
 }
 
 @Test
 public void testIsParameter() {
 // create an instance of the tested class
 CommandLine cmd = new CommandLine(new String[]{"-a", "b"});
 
 assertFalse(cmd.isParameter("a"));
 assertTrue(cmd.isParameter("b"));
 }
 
 @Test
 public void testValue() {
 // create an instance of the tested class
 CommandLine cmd = new CommandLine(new String[]{"-a", "b"});
 
 assertEquals(null, cmd.value("a"));
 assertEquals("b", cmd.value("b"));
 assertEquals("default", cmd.value("c", "default"));
 }
 
 @Test
 public void testAdd() {
 // create an instance of the tested class
 CommandLine cmd = new CommandLine();
 
 assertTrue(cmd.add("a", null)); // Adding option a
 assertFalse(cmd.add("a", null, false)); // Trying to add existing o[1D[4D[K
o[1D[K
 option a without overwrite
 assertTrue(cmd.add("b", "value")); // Adding parameter b with value[5D[8D[K
value[5D[K
 value
 
 assertFalse(cmd.add("c", null, false)); // Trying to add new parame[6D[9D[K
parame[6D[K
 parameter c without overwrite
 assertTrue(cmd.add("c", "newValue")); // Overwriting existing param[5D[8D[K
param[5D[K
 parameter c
 }
}