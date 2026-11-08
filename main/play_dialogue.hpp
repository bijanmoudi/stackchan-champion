// StackChan Champion: stable audio clip IDs for the fully offline toddler game.
// The ordering MUST match CLIPS in tools/generate_play_audio.py.
// Each spoken response is a COMPLETE sentence, not a stitched list of words;
// this preserves natural rhythm for human-recorded clips.
#pragma once
namespace stackchan::app::play_dialogue {
enum Clip : int {
    Dali=0, Red, Blue, Yellow, Bravo, Try,
    FindRed, FindBlue, FindYellow, IntroColors,
    StartRed, StartBlue, StartYellow,
    CorrectRedThenBlue, CorrectRedThenYellow,
    CorrectBlueThenRed, CorrectBlueThenYellow,
    CorrectYellowThenRed, CorrectYellowThenBlue,
    WrongRedForBlue, WrongRedForYellow,
    WrongBlueForRed, WrongBlueForYellow,
    WrongYellowForRed, WrongYellowForBlue,
    Count
};
constexpr int initial(int target) {
    return (target >= 0 && target < 3) ? StartRed + target : -1;
}
constexpr int correct(int chosen, int next) {
    constexpr int table[3][3] = {
        {-1, CorrectRedThenBlue, CorrectRedThenYellow},
        {CorrectBlueThenRed, -1, CorrectBlueThenYellow},
        {CorrectYellowThenRed, CorrectYellowThenBlue, -1}
    };
    return (chosen >= 0 && chosen < 3 && next >= 0 && next < 3)
         ? table[chosen][next] : -1;
}
constexpr int incorrect(int chosen, int target) {
    constexpr int table[3][3] = {
        {-1, WrongRedForBlue, WrongRedForYellow},
        {WrongBlueForRed, -1, WrongBlueForYellow},
        {WrongYellowForRed, WrongYellowForBlue, -1}
    };
    return (chosen >= 0 && chosen < 3 && target >= 0 && target < 3)
         ? table[chosen][target] : -1;
}
static_assert(initial(0) == 10 && initial(2) == 12);
static_assert(correct(2, 0) == 17);
static_assert(incorrect(1, 2) == 22);
} // namespace stackchan::app::play_dialogue
