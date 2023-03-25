base.metadata.organizationId = "orgID";
base.metadata.description = "Configuration for ignoring open file events for Linux for ICM icmID";
base.metadata.groupId = "IgnoreOpenFileEvents";

// Find "host" configuration index
indexOfHostConfigType = ArrayUtils.findIndex(base.data.configTypes, "configType", "host");

// Turn on feature
ArrayUtils.addOrReplaceMultiple(base.data.configTypes[indexOfHostConfigType].capabilities, "name", [
    {
        "name":"IgnoreOpenFileEvents",
        "enabledUpToRing": "Production",
        //"owner": "owner_full_name"
    }]);
