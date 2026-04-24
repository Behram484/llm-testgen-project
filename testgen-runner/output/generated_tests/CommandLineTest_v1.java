package org.exolab.jms.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CommandLineTest_v1 {
 @Test
 public void testExists() {
 CommandLine commandLine = new CommandLine(new String[] {"--existing[12D[K
{"--existingOption", "paramName=paramValue"});
 assertTrue(commandLine.exists("existingOption"));
 assertFalse(commandLine.exists("nonExistingOption"));
 }

 @Test
 public void testIsSwitch() {
 CommandLine commandLine = new CommandLine(new String[] {"--switch"}[12D[K
{"--switch"});
 assertTrue(commandLine.isSwitch("switch"));
 assertFalse(commandLine.isSwitch("nonExistingSwitch"));
 }

 @Test
 public void testIsParameter() {
 CommandLine commandLine = new CommandLine(new String[] {"paramName=[12D[K
{"paramName=paramValue"});
 assertTrue(commandLine.isParameter("paramName"));
 assertFalse(commandLine.isParameter("nonExistingParam"));
 }

 @Test
 public void testValue() {
 CommandLine commandLine = new CommandLine(new String[] {"--existing[12D[K
{"--existingOption", "paramName=paramValue"});
 assertEquals("paramValue", commandLine.value("paramName"));
 assertNull(commandLine.value("nonExistingParam"));
 }

 @Test
 public void testAdd() {
 CommandLine commandLine = new CommandLine();
 
 // Add an option and parameter
 assertTrue(commandLine.add("option", null));
 assertTrue(commandLine.add("paramName", "paramValue"));
 
 // Try to add the same again without overwrite, should fail
 assertFalse(commandLine.add("option", null, false));
 assertFalse(commandLine.add("paramName", "newParamValue", false));
 
 // Now try with overwrite which will succeed
 assertTrue(commandLine.add("option", null, true));
 assertTrue(commandLine.add("paramName", "newParamValue", true));
 }
}