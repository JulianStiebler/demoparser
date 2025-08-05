from dataclasses import dataclass, field
from typing import Optional, List

class DotSeparatedString(str):
    """
    A string that represents a dot-separated value.
    """
    @property
    def parts(self) -> list[str]:
        """Returns a list of strings split by the dot separator."""
        return self.split('.')

    def __repr__(self):
        return f"DotSeparatedString({super().__repr__()})"
    
@dataclass
class Header:
    server_name: str
    demo_file_stamp: str
    network_protocol: int
    map_name: str
    fullpackets_version: int
    allow_clientside_entities: bool
    allow_clientside_particles: bool
    demo_version_name: str
    demo_version_guid: str
    client_name: str
    game_directory: str
    addons: DotSeparatedString = field(default_factory=DotSeparatedString)

    @property
    def addons_list(self) -> List[str]:
        return self.addons.parts


@dataclass
class VoiceData:
    """
    Container for voice data from parse_voice().
    Maps Steam IDs to voice audio bytes.
    """
    voice_clips: dict[str, bytes]  # steamid -> audio bytes
    
    @property
    def player_count(self) -> int:
        """Number of players with voice data."""
        return len(self.voice_clips)
    
    @property
    def player_ids(self) -> List[str]:
        """List of Steam IDs with voice data."""
        return list(self.voice_clips.keys())
    
    @property
    def total_audio_size(self) -> int:
        """Total size of all voice clips in bytes."""
        return sum(len(clip) for clip in self.voice_clips.values())
    
    def get_player_voice(self, steamid: str) -> Optional[bytes]:
        """Get voice data for a specific player."""
        return self.voice_clips.get(steamid)
    
    def has_voice_data(self, steamid: str) -> bool:
        """Check if player has voice data."""
        return steamid in self.voice_clips

    def export_wav(self, steamid: str):
        try:
            import io
            from pydub import AudioSegment
        except ImportError:
            return

        clip_bytes = self.get_player_voice(steamid)
        if not clip_bytes:
            print(f"No voice data found for Steam ID: {steamid}")
            return

        try:
            audio_file = io.BytesIO(clip_bytes)
            audio_segment = AudioSegment.from_wav(audio_file)
            with open("test.wav", "wb") as temp_file:
                audio_segment.export(temp_file, format="wav")
            
        except Exception as e:
            print(f"Error playing audio for {steamid}: {e}")
