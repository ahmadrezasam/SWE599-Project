import { FilterParams } from "../interfaces/filter";

export class Earthquake {
  id: number;
  event_id: string;
  date: string;
  origin_time: string;
  latitude: number;
  longitude: number;
  magnitude: number;
  depth: number;
  location: string;

  constructor(
    id: number,
    event_id: string,
    date: string,
    origin_time: string,
    latitude: number,
    longitude: number,
    magnitude: number,
    depth: number,
    location: string
  ) {
    this.id = id;
    this.event_id = event_id;
    this.date = date;
    this.origin_time = origin_time;
    this.latitude = latitude;
    this.longitude = longitude;
    this.magnitude = magnitude;
    this.depth = depth;
    this.location = location;
  }

  static applyFilters(earthquakes: Earthquake[], filterParams: FilterParams): Earthquake[] {
    const {
      latitude__gt,
      latitude__lt,
      longitude__gt,
      longitude__lt,
      magnitude__gt,
      magnitude__lt,
      depth__gt,
      depth__lt,
    } = filterParams;
  
    return earthquakes.filter((earthquake: Earthquake) => {
      return (
        (!latitude__gt || earthquake.latitude >= parseFloat(latitude__gt)) &&
        (!latitude__lt || earthquake.latitude <= parseFloat(latitude__lt)) &&
        (!longitude__gt || earthquake.longitude >= parseFloat(longitude__gt)) &&
        (!longitude__lt || earthquake.longitude <= parseFloat(longitude__lt)) &&
        (!magnitude__gt || earthquake.magnitude >= parseFloat(magnitude__gt)) &&
        (!magnitude__lt || earthquake.magnitude <= parseFloat(magnitude__lt)) &&
        (!depth__gt || earthquake.depth >= parseFloat(depth__gt)) &&
        (!depth__lt || earthquake.depth <= parseFloat(depth__lt))
      );
    });
  };

  static async fetchEarthquakeData (apiUrl: string,  filterParams?: FilterParams): Promise<Earthquake[]> {
    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      const earthquakeObjects = data.map((quake: any) => new Earthquake(
        quake.id,
        quake.event_id,
        quake.date,
        quake.origin_time,
        quake.latitude,
        quake.longitude,
        quake.magnitude,
        quake.depth,
        quake.location
      ));
      
      if (filterParams) {
        return this.applyFilters(earthquakeObjects, filterParams);
      }
      
      return earthquakeObjects;
    } catch (error) {
      console.error("Error fetching earthquake data:", error);
      return []; // Return an empty array or handle the error as needed
    }
  };
}
