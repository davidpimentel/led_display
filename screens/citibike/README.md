## Setup Citibike

First, use Citibike's API to find your station ID:


```
curl https://gbfs.citibikenyc.com/gbfs/es/station_information.json | jq '.data.stations[] | select (.name == "E 7 St & Avenue A")'
```

you might have to grep through the file a bit to find the station. My Station is "E 7 St & Avenue A", but the names aren't consistent / predictable.

## Citibike station ids
  station_id: "432"  # A and 7th
  station_id: "3101"  # bedford
  station_id: "3108"  # Nassau