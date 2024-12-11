:::mermaid
flowchart TD
    TYPE_SHOU -->CAM_BROAD
    TYPE_SYST -->CAM_BROAD
    TYPE_BBLB -->CAM_BROAD
    TYPE_SLOW -->CAM_BROAD
    TYPE_CINE -->CAM_CINE_OR_XCH
    TYPE_MIRR -->CAM_CINE_OR_XCH
    TYPE_MINI_XCH-->CAM_MINI_XCH
    TYPE_MINI_FIXNOXCH -->|No Lens X|CAM_NOXCH
    TYPE_MINI_WITHIZF-->|IZF integrated|CAM_IZFNOX
    TYPE_HAND-->CAM_IZFNOX[IZF integrated]
    TYPE_PTZ-->CAM_IZFNOX
    subgraph Camera Type
        TYPE_SHOU(Shoulder)
        TYPE_SYST(System)
        TYPE_BBLB(BBlock)
        TYPE_SLOW(Slow Motion)
        TYPE_MIRR(Mirrorless)
        TYPE_CINE(CineStyle)
        TYPE_MINI_WITHIZF(Minicam IZT)
        TYPE_HAND(Handheld)
        TYPE_PTZ(PTZ)
        TYPE_MINI_FIXNOXCH(Minicam FIX)
        TYPE_MINI_XCH(Minicam XCH)

    end
    subgraph Camera Property
        CAM_BROAD[Broadcast]
        CAM_NOXCH[Fixed Lens]
        CAM_IZFNOX[IZF integrated]
        CAM_CINE_OR_XCH[CineStyle<br>Mirrorless<br>XCHangeable]
        CAM_MINI_XCH(Mini Lens)
    end
    CAM_BROAD-->LENS_B4_1
    CAM_CINE_OR_XCH-->|URSA \nor \nCanon|LENS_B4_2
    CAM_CINE_OR_XCH-->|URSA \nor \nCanon|LENS_CINESER_2
    CAM_CINE_OR_XCH-->|/URSA \nand \n/Canon|LENS_B4_3
    CAM_CINE_OR_XCH-->|/URSA \nand \n/Canon|LENS_CINESER_3
    CAM_CINE_OR_XCH-->LENS_EMOUNT
    CAM_CINE_OR_XCH-->LENS_CABRIO
    CAM_CINE_OR_XCH-->LENS_NONMOT_ARRI
    CAM_CINE_OR_XCH-->LENS_NONMOT_TILT
    CAM_CINE_OR_XCH-->LENS_MANUAL
    CAM_NOXCH-->LENS_MANUAL
    CAM_IZFNOX-->LENS_INTER
    CAM_MINI_XCH-->LENS_MANUAL
    CAM_MINI_XCH-->|AtomOne|LENS_DCHIP_MOT

    subgraph USER Lens Choice
        direction TB
        LENS_B4_1[B4-Lens 1]
        LENS_B4_2[B4-Lens 2]
        LENS_B4_3[B4-Lens 3]
        LENS_CABRIO[Cabrio]
        LENS_CINESER_2[CineServo 2]
        LENS_CINESER_3[CineServo 3]
        LENS_EMOUNT[E-Mount]
        LENS_NONMOT_ARRI[Non Motorized\nand ARRI motors]
        LENS_NONMOT_TILT[Non Motorized\nand TILTA motors]
        LENS_DCHIP_MOT[Dreamchip motor]
        LENS_MANUAL["Manual"]
        LENS_INTER["Integrated IZF"]
    end
    LENS_B4_1-->|Iris|THROU_CAM_1
    LENS_B4_1-->|IZF|CABLE_B4_1
    LENS_NONMOT_TILT-->CABLE_TILTA
    LENS_NONMOT_ARRI-->CABLE_ARRI[Arri\nCForce cable]
    LENS_MANUAL-->NO_CONTROL
    LENS_CABRIO-->CABLE_B4_FUJI
    LENS_CINESER_2-->THROU_CAM_2
    LENS_CINESER_3-->|Iris|THROU_CAM_3
    LENS_CINESER_3-->|IZF|CABLE_B4_3
    LENS_EMOUNT-->|Iris|THROU_CAM_4
    LENS_EMOUNT-->|IZF|CABLE_TILTA_4
    LENS_B4_2-->THROU_CAM_2
    LENS_B4_3-->|Iris|THROU_CAM_3
    LENS_B4_3-->|IZF|CABLE_B4_3
    LENS_INTER-->THROU_CAM_INTER[Through<br>camera]
    LENS_DCHIP_MOT-->THROU_CAM_DCHIP[Through<br>camera]
    subgraph Control
       CABLE_B4_1[Cyanview\nB4 cable]
       CABLE_B4_3[Cyanview\nB4 cable]
       CABLE_B4_FUJI[Cyanview\nB4+FUJI\ncables]
       CABLE_TILTA[Cyanview\nTilta cable]
       CABLE_TILTA_4[Cyanview\nTilta cable]
       CABLE_ARRI
       THROU_CAM_1[Through<br>camera]
       THROU_CAM_2[Through<br>camera]
       THROU_CAM_3[Through<br>camera]
       THROU_CAM_4[Through<br>camera]
       THROU_CAM_INTER[Through<br>camera]
       THROU_CAM_DCHIP[Through<br>Camera]
       NO_CONTROL[No lens\ncontrol]
    end
:::
