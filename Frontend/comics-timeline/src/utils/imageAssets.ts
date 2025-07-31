/**
 * Static Image Asset Manager
 * Manually import and map comic event images for reliable access
 */

// Import known images
import crisisOnInfiniteEarthsImg from '../assets/crisis_on_infinite_earths.webp'
import zeroHourImg from '../assets/zero_hour.avif' 
import infiniteCrisisImg from '../assets/infinite_crisis.jpg'
import finalCrisisImg from '../assets/final_crisis.webp'
import flashpointImg from '../assets/flashpoint.avif'
import rebirthImg from '../assets/rebirth.webp' 
import doomsdayClockImg from '../assets/doomsday_clock.webp' 

import fantasticFourImg from '../assets/creation_of_the_fantastic_four.webp'
import secretWars1984Img from '../assets/secret_wars_1984.jpg' 
import onslaughtImg from '../assets/onslaught.jpg' 
import secretWars2015Img from '../assets/secret_wars_2015.webp' 

// Image mapping - add new images here as they become available
const imageMap: Record<string, string> = {
  // DC Events  
  'crisis_on_infinite_earths': crisisOnInfiniteEarthsImg,
  'zero_hour': zeroHourImg,
  'infinite_crisis': infiniteCrisisImg,
  'final_crisis': finalCrisisImg,
  'flashpoint': flashpointImg,
  'rebirth': rebirthImg,
  'doomsday_clock': doomsdayClockImg,

  // Marvel Events
  'creation_of_the_fantastic_four': fantasticFourImg,
  'secret_wars_1984': secretWars1984Img,
  'onslaught': onslaughtImg,
  'secret_wars_2015': secretWars2015Img,
}


export const eventToFilename = (eventName: string): string => {
  return eventName
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '') // Remove special characters
    .replace(/\s+/g, '_') // Replace spaces with underscores
    .trim()
}

export const getEventImage = (eventName: string): string | null => {
  const filename = eventToFilename(eventName)
  return imageMap[filename] || null
}

export const getImageByFilename = (filename: string): string | null => {
  return imageMap[filename] || null
}

export const getAvailableImages = (): string[] => {
  return Object.keys(imageMap)
}


export const hasImage = (filename: string): boolean => {
  return filename in imageMap
}

// Export the raw image assets object for debugging
export { imageMap as imageAssets }

// Log available images for debugging
console.log('Available comic event images:', getAvailableImages())
