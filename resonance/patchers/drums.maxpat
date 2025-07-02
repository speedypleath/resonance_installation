{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 6,
			"revision" : 5,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 34.0, 87.0, 975.0, 715.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "",
		"showontab" : 1,
		"assistshowspatchername" : 0,
		"boxes" : [ 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "multichannelsignal" ],
					"patching_rect" : [ 546.0, 580.0, 70.0, 22.0 ],
					"text" : "mc.pack~ 2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-2",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 546.0, 631.0, 108.0, 22.0 ],
					"text" : "mc.send~ drums 2"
				}

			}
, 			{
				"box" : 				{
					"autosave" : 1,
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"id" : "obj-53",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 8,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal", "signal", "", "list", "int", "", "", "" ],
					"patching_rect" : [ 546.0, 462.0, 300.0, 100.0 ],
					"save" : [ "#N", "vst~", "loaduniqueid", 0, "C74_AU:/kHs Compressor", ";" ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_invisible" : 1,
							"parameter_longname" : "vst~[1]",
							"parameter_modmode" : 0,
							"parameter_shortname" : "vst~[1]",
							"parameter_type" : 3
						}

					}
,
					"saved_object_attributes" : 					{
						"parameter_enable" : 1,
						"parameter_mappable" : 0
					}
,
					"snapshot" : 					{
						"filetype" : "C74Snapshot",
						"version" : 2,
						"minorversion" : 0,
						"name" : "snapshotlist",
						"origin" : "vst~",
						"type" : "list",
						"subtype" : "Undefined",
						"embed" : 1,
						"snapshot" : 						{
							"pluginname" : "kHs Compressor.auinfo",
							"plugindisplayname" : "kHs Compressor",
							"pluginsavedname" : "C74_AU:/kHs Compressor",
							"pluginsaveduniqueid" : 711806331,
							"version" : 1,
							"isbank" : 0,
							"isbase64" : 1,
							"sliderorder" : [  ],
							"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
							"blob" : "802.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBXHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HKBwEAtjfz.+tGRJIamkGg+KFPyO4vOReddY4Bl11PJ1Ot6kkKVvZnVdTE7Seuf8kvyCT5qqIesTef6HS33ImMNjiWOUmL7GTTStTvEoopZoQpk+erdKW4mChd5nx9zwAGIjdo0j95jTb7Iqqmm5s4C6PIEjorKQ+0rTz4bNyKaHQGWZtbCjkVXrl4NX35xM52ssSUtbIklgX3nWYCW63kPgUmX58VWYarSJ6CoC+iOUyAS2caSTwCo6Vdo+MWaQYC2tkqKZbWor.2chB4tedtzm93lpKhtGoa9WHUhqSOdg2VyaiNAU5XoxTeAFfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX9TL4e+WIkYh5e8l4kKsukyShml2SSSa3ppsG1TeXeoorPmi7cVUyT15M0qqpNLF5x8JGTupptdy80aGqmm6wb4Ah2OsRRQb+3MXUpAUeupd2lwLdHvGG3vbz861tae89DsrLVdr.GeixKkZjg285vF3gtbkVtHXcO+se5hZ+c+IZDcq58hgwUMOYh2jNeDORt73QNeF9lhk46Rq0o4km4poySEOUlARV05c0yMQSA93694kuBTKc.BtXpww.f...v94...PsT.B...T..BHf..7nn3Z4hoFGC.B...6mC..n.......................LGcgQWYtn1bu4FTKUfA.....D..A..N....3H......RDVclgmDqM2XvAQ..f..U.fF.bB.r.PL.jC.AAPS.Hk.bKP3BXN.......f.A.........PC..................f.nC"
						}
,
						"snapshotlist" : 						{
							"current_snapshot" : 0,
							"entries" : [ 								{
									"filetype" : "C74Snapshot",
									"version" : 2,
									"minorversion" : 0,
									"name" : "kHs Compressor",
									"origin" : "kHs Compressor.auinfo",
									"type" : "AudioUnit",
									"subtype" : "AudioEffect",
									"embed" : 0,
									"snapshot" : 									{
										"pluginname" : "kHs Compressor.auinfo",
										"plugindisplayname" : "kHs Compressor",
										"pluginsavedname" : "C74_AU:/kHs Compressor",
										"pluginsaveduniqueid" : 711806331,
										"version" : 1,
										"isbank" : 0,
										"isbase64" : 1,
										"sliderorder" : [  ],
										"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
										"blob" : "802.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBXHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HKBwEAtjfz.+tGRJIamkGg+KFPyO4vOReddY4Bl11PJ1Ot6kkKVvZnVdTE7Seuf8kvyCT5qqIesTef6HS33ImMNjiWOUmL7GTTStTvEoopZoQpk+erdKW4mChd5nx9zwAGIjdo0j95jTb7Iqqmm5s4C6PIEjorKQ+0rTz4bNyKaHQGWZtbCjkVXrl4NX35xM52ssSUtbIklgX3nWYCW63kPgUmX58VWYarSJ6CoC+iOUyAS2caSTwCo6Vdo+MWaQYC2tkqKZbWor.2chB4tedtzm93lpKhtGoa9WHUhqSOdg2VyaiNAU5XoxTeAFfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX9TL4e+WIkYh5e8l4kKsukyShml2SSSa3ppsG1TeXeoorPmi7cVUyT15M0qqpNLF5x8JGTupptdy80aGqmm6wb4Ah2OsRRQb+3MXUpAUeupd2lwLdHvGG3vbz861tae89DsrLVdr.GeixKkZjg285vF3gtbkVtHXcO+se5hZ+c+IZDcq58hgwUMOYh2jNeDORt73QNeF9lhk46Rq0o4km4poySEOUlARV05c0yMQSA93694kuBTKc.BtXpww.f...v94...PsT.B...T..BHf..7nn3Z4hoFGC.B...6mC..n.......................LGcgQWYtn1bu4FTKUfA.....D..A..N....3H......RDVclgmDqM2XvAQ..f..U.fF.bB.r.PL.jC.AAPS.Hk.bKP3BXN.......f.A.........PC..................f.nC"
									}
,
									"fileref" : 									{
										"name" : "kHs Compressor",
										"filename" : "kHs Compressor_20250620.maxsnap",
										"filepath" : "~/Documents/Max 8/Projects/Resonance/data",
										"filepos" : -1,
										"snapshotfileid" : "5e9db4fbb2a52ed12f3899d8eb803b2d"
									}

								}
 ]
						}

					}
,
					"text" : "vst~ \"C74_AU:/kHs Compressor\"",
					"varname" : "vst~",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-49",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 228.0, 76.0, 38.0, 22.0 ],
					"text" : "s kick"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-48",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 228.0, 12.0, 113.0, 22.0 ],
					"text" : "metro 4n @active 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-47",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 297.0, 368.0, 33.0, 22.0 ],
					"text" : "+~ 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-46",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 297.0, 323.0, 36.0, 22.0 ],
					"text" : "%~ 3"
				}

			}
, 			{
				"box" : 				{
					"args" : [ "global" ],
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-43",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "rtt.clock.maxpat",
					"numinlets" : 4,
					"numoutlets" : 2,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 53.0, 29.0, 145.0, 45.0 ],
					"varname" : "global",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-27",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 143.0, 111.0, 203.0, 22.0 ],
					"text" : "rtt.euclidean~ @steps 12 @events 7"
				}

			}
, 			{
				"box" : 				{
					"fontface" : 0,
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : "obj-39",
					"maxclass" : "number~",
					"mode" : 2,
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "float" ],
					"patching_rect" : [ 105.5, 323.0, 56.0, 22.0 ],
					"sig" : 0.0
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-38",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 367.0, 516.0, 38.0, 22.0 ],
					"text" : "s tom"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-37",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 304.0, 516.0, 44.0, 22.0 ],
					"text" : "s hihat"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-36",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 243.0, 516.0, 48.0, 22.0 ],
					"text" : "s snare"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-35",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "bang" ],
					"patching_rect" : [ 304.0, 462.0, 42.0, 22.0 ],
					"text" : "edge~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-34",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "bang" ],
					"patching_rect" : [ 367.0, 462.0, 42.0, 22.0 ],
					"text" : "edge~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-33",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "bang" ],
					"patching_rect" : [ 372.0, 306.0, 44.0, 22.0 ],
					"text" : "line~ 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-31",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "bang" ],
					"patching_rect" : [ 243.0, 462.0, 42.0, 22.0 ],
					"text" : "edge~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-23",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 3,
					"outlettype" : [ "signal", "signal", "signal" ],
					"patching_rect" : [ 297.0, 408.0, 49.0, 22.0 ],
					"text" : "gate~ 3"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-7",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 22.5, 438.0, 77.0, 22.0 ],
					"text" : "clientwindow"
				}

			}
, 			{
				"box" : 				{
					"active" : 					{
						"global::m::transportstate" : 1
					}
,
					"id" : "obj-22",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 22.5, 466.0, 198.0, 22.0 ],
					"saved_object_attributes" : 					{
						"client_rect" : [ 580, 87, 949, 304 ],
						"parameter_enable" : 0,
						"parameter_mappable" : 0,
						"storage_rect" : [ 583, 69, 1034, 197 ]
					}
,
					"text" : "pattrstorage randomiser @greedy 1",
					"varname" : "randomiser[1]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-6",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "", "", "" ],
					"patching_rect" : [ 53.0, 111.0, 71.5, 22.0 ],
					"text" : "rtt.loop~",
					"varname" : "loop_37921"
				}

			}
, 			{
				"box" : 				{
					"args" : [ "randomiser" ],
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-1",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "rtt.dist.maxpat",
					"numinlets" : 1,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "" ],
					"patching_rect" : [ 105.0, 177.0, 292.0, 105.0 ],
					"varname" : "randomiser",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-30",
					"maxclass" : "newobj",
					"numinlets" : 6,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 422.0, 255.0, 105.0, 22.0 ],
					"text" : "scale -1. 1. -10. 0."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-29",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "float" ],
					"patching_rect" : [ 422.0, 209.0, 88.0, 22.0 ],
					"text" : "snapshot~ 100"
				}

			}
, 			{
				"box" : 				{
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"enablehscroll" : 0,
					"enablevscroll" : 0,
					"id" : "obj-28",
					"lockeddragscroll" : 0,
					"lockedsize" : 0,
					"maxclass" : "bpatcher",
					"name" : "custom.lfo.maxpat",
					"numinlets" : 0,
					"numoutlets" : 1,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 422.0, 7.0, 343.0, 188.0 ],
					"varname" : "custom.lfo",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-19",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 6,
							"revision" : 5,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 0.0, 26.0, 975.0, 689.0 ],
						"bglocked" : 0,
						"openinpresentation" : 0,
						"default_fontsize" : 12.0,
						"default_fontface" : 0,
						"default_fontname" : "Arial",
						"gridonopen" : 1,
						"gridsize" : [ 15.0, 15.0 ],
						"gridsnaponopen" : 1,
						"objectsnaponopen" : 1,
						"statusbarvisible" : 2,
						"toolbarvisible" : 1,
						"lefttoolbarpinned" : 0,
						"toptoolbarpinned" : 0,
						"righttoolbarpinned" : 0,
						"bottomtoolbarpinned" : 0,
						"toolbars_unpinned_last_save" : 0,
						"tallnewobj" : 0,
						"boxanimatetime" : 200,
						"enablehscroll" : 1,
						"enablevscroll" : 1,
						"devicewidth" : 0.0,
						"description" : "",
						"digest" : "",
						"tags" : "",
						"style" : "",
						"subpatcher_template" : "",
						"showontab" : 1,
						"assistshowspatchername" : 0,
						"boxes" : [ 							{
								"box" : 								{
									"id" : "obj-6",
									"maxclass" : "button",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 454.0, 90.0, 24.0, 24.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-10",
									"int" : 1,
									"maxclass" : "gswitch2",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 287.0, 163.0, 39.0, 32.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-9",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "int" ],
									"patching_rect" : [ 320.0, 129.0, 32.0, 22.0 ],
									"text" : "< 50"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-7",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 320.0, 101.0, 73.0, 22.0 ],
									"text" : "random 100"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "preset",
									"numinlets" : 1,
									"numoutlets" : 5,
									"outlettype" : [ "preset", "int", "preset", "int", "" ],
									"patching_rect" : [ 701.0, 352.0, 100.0, 40.0 ],
									"preset_data" : [ 										{
											"number" : 1,
											"data" : [ 5, "<invalid>", "flonum", "float", 40.0, 5, "<invalid>", "flonum", "float", 881.0, 6, "<invalid>", "gain~", "list", 96, 10.0 ]
										}
, 										{
											"number" : 2,
											"data" : [ 5, "<invalid>", "flonum", "float", 1.820000052452087, 5, "<invalid>", "flonum", "float", 673.0, 6, "<invalid>", "gain~", "list", 27, 10.0 ]
										}
 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-15",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 359.0, 507.0, 34.0, 22.0 ],
									"text" : "limi~"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-13",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 742.0, 168.0, 135.0, 22.0 ],
									"saved_object_attributes" : 									{
										"client_rect" : [ 580, 87, 949, 304 ],
										"parameter_enable" : 0,
										"parameter_mappable" : 0,
										"storage_rect" : [ 583, 69, 1034, 197 ]
									}
,
									"text" : "pattrstorage @greedy 1",
									"varname" : "u856003620"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-11",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 4,
									"outlettype" : [ "", "", "", "" ],
									"patching_rect" : [ 779.0, 241.0, 56.0, 22.0 ],
									"text" : "autopattr",
									"varname" : "u028002892"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-3",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 248.0, 543.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-1",
									"maxclass" : "newobj",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 246.0, 29.0, 36.0, 22.0 ],
									"text" : "r tom"
								}

							}
, 							{
								"box" : 								{
									"bgmode" : 0,
									"border" : 0,
									"clickthrough" : 0,
									"embed" : 1,
									"enablehscroll" : 0,
									"enablevscroll" : 0,
									"id" : "obj-2",
									"lockeddragscroll" : 0,
									"lockedsize" : 0,
									"maxclass" : "bpatcher",
									"name" : "custom.drum.maxpat",
									"numinlets" : 2,
									"numoutlets" : 1,
									"offset" : [ 0.0, 0.0 ],
									"outlettype" : [ "signal" ],
									"patcher" : 									{
										"fileversion" : 1,
										"appversion" : 										{
											"major" : 8,
											"minor" : 6,
											"revision" : 5,
											"architecture" : "x64",
											"modernui" : 1
										}
,
										"classnamespace" : "box",
										"rect" : [ 47.0, 87.0, 683.0, 701.0 ],
										"bglocked" : 0,
										"openinpresentation" : 1,
										"default_fontsize" : 12.0,
										"default_fontface" : 0,
										"default_fontname" : "Arial",
										"gridonopen" : 1,
										"gridsize" : [ 15.0, 15.0 ],
										"gridsnaponopen" : 2,
										"objectsnaponopen" : 1,
										"statusbarvisible" : 2,
										"toolbarvisible" : 1,
										"lefttoolbarpinned" : 0,
										"toptoolbarpinned" : 0,
										"righttoolbarpinned" : 0,
										"bottomtoolbarpinned" : 0,
										"toolbars_unpinned_last_save" : 0,
										"tallnewobj" : 0,
										"boxanimatetime" : 200,
										"enablehscroll" : 1,
										"enablevscroll" : 1,
										"devicewidth" : 0.0,
										"description" : "",
										"digest" : "",
										"tags" : "",
										"style" : "",
										"subpatcher_template" : "<none>",
										"assistshowspatchername" : 0,
										"boxes" : [ 											{
												"box" : 												{
													"id" : "obj-40",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 227.0, 54.0, 22.0 ],
													"text" : "deferlow"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-36",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 297.0, 65.0, 22.0 ],
													"saved_object_attributes" : 													{
														"filename" : "resize.js",
														"parameter_enable" : 0
													}
,
													"text" : "js resize.js"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-33",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 195.0, 95.0, 22.0 ],
													"text" : "loadmess resize"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-11",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "" ],
													"patching_rect" : [ 675.0, 615.0, 67.0, 22.0 ],
													"save" : [ "#N", "thispatcher", ";", "#Q", "end", ";" ],
													"text" : "thispatcher"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-45",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1010.75, 87.0, 32.0, 22.0 ],
													"text" : "gate"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-46",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 1010.75, 156.0, 29.5, 22.0 ],
													"text" : "+ 1"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-47",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1010.75, 120.0, 66.0, 22.0 ],
													"text" : "random 16"
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-43",
													"index" : 2,
													"maxclass" : "inlet",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 957.75, 142.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-42",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 270.0, 330.0, 148.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 143.0, 36.25, 74.0, 21.0 ],
													"text" : "Randomize"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-39",
													"maxclass" : "live.toggle",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1010.75, 52.5, 15.0, 15.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 219.0, 37.125, 19.0, 19.25 ],
													"saved_attribute_attributes" : 													{
														"activebgoncolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_enum" : [ "off", "on" ],
															"parameter_longname" : "live.toggle[5]",
															"parameter_mmax" : 1,
															"parameter_modmode" : 0,
															"parameter_shortname" : "live.toggle",
															"parameter_type" : 2
														}

													}
,
													"varname" : "randomize"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 13.0,
													"id" : "obj-38",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 791.5, 14.5, 196.0, 23.0 ],
													"text" : "pattrstorage presetPattrstorage"
												}

											}
, 											{
												"box" : 												{
													"attr" : "bubblesize",
													"id" : "obj-37",
													"maxclass" : "attrui",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"parameter_enable" : 0,
													"patching_rect" : [ 615.0, 15.0, 150.0, 22.0 ]
												}

											}
, 											{
												"box" : 												{
													"active1" : [ 1.0, 0.709803921568627, 0.196078431372549, 1.0 ],
													"bubblesize" : 14,
													"id" : "obj-35",
													"maxclass" : "preset",
													"numinlets" : 1,
													"numoutlets" : 5,
													"outlettype" : [ "preset", "int", "preset", "int", "" ],
													"patching_rect" : [ 615.0, 146.0, 100.0, 40.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 246.0, 36.25, 150.0, 77.5 ],
													"preset_data" : [ 														{
															"number" : 1,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 116, 5, "obj-71", "live.dial", "float", 46.0, 5, "obj-74", "live.dial", "float", 850.0, 5, "obj-77", "live.dial", "float", 10.0, 5, "obj-79", "live.dial", "float", 10.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
, 														{
															"number" : 2,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 123, 5, "obj-71", "live.dial", "float", 47.0, 5, "obj-74", "live.dial", "float", 725.0, 5, "obj-77", "live.dial", "float", 10.0, 5, "obj-79", "live.dial", "float", 10.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14 ]
														}
, 														{
															"number" : 3,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 48, 5, "obj-71", "live.dial", "float", 31.0, 5, "obj-74", "live.dial", "float", 750.0, 5, "obj-77", "live.dial", "float", 22.5, 5, "obj-79", "live.dial", "float", 8.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
, 														{
															"number" : 4,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 130, 5, "obj-71", "live.dial", "float", 48.0, 5, "obj-74", "live.dial", "float", 575.0, 5, "obj-77", "live.dial", "float", 15.0, 5, "obj-79", "live.dial", "float", 10.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-34",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 204.0, 180.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 129.0, 60.0, 21.0 ],
													"text" : "Output",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-32",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 240.0, 135.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 339.0, 0.0, 81.0, 21.0 ],
													"text" : "Select Preset",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-19",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 285.0, 195.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 0.0, 64.0, 21.0 ],
													"text" : "Trigger",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-3",
													"index" : 1,
													"maxclass" : "inlet",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "bang" ],
													"patching_rect" : [ 390.0, 45.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-26",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 4,
													"outlettype" : [ "", "", "", "" ],
													"patching_rect" : [ 525.0, 146.0, 56.0, 22.0 ],
													"restore" : 													{
														"button" : [ 1.0 ],
														"exponent[1]" : [ 10.0 ],
														"gain" : [ 1.0 ],
														"number" : [ 130 ],
														"peakdown[3]" : [ 15.0 ],
														"peakright[3]" : [ 575.0 ],
														"pitch[3]" : [ 48.0 ],
														"randomize" : [ 0.0 ]
													}
,
													"text" : "autopattr",
													"varname" : "u477009426"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-5",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 390.0, 161.0, 103.0, 22.0 ],
													"saved_object_attributes" : 													{
														"client_rect" : [ 580, 87, 949, 304 ],
														"parameter_enable" : 0,
														"parameter_mappable" : 0,
														"storage_rect" : [ 583, 69, 1034, 197 ]
													}
,
													"text" : "pattrstorage drum",
													"varname" : "drum"
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-2",
													"index" : 1,
													"maxclass" : "outlet",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 175.0, 660.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-85",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 957.75, 442.0, 155.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 22.0, 29.5, 155.0, 21.0 ],
													"text" : "Drum Generator"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-80",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 808.0, 227.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-79",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1010.75, 540.0, 45.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 66.0, 66.75, 44.0, 48.0 ],
													"prototypename" : "gain",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_initial" : [ 10 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "exponent[1]",
															"parameter_mmax" : 20.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Exponent",
															"parameter_steps" : 21,
															"parameter_type" : 1,
															"parameter_unitstyle" : 0
														}

													}
,
													"varname" : "exponent[1]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-78",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 915.0, 282.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-77",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1056.75, 540.0, 57.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 116.0, 66.75, 49.0, 48.0 ],
													"prototypename" : "time",
													"saved_attribute_attributes" : 													{
														"textcolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_initial" : [ 10.0 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "peakdown[3]",
															"parameter_mmax" : 50.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Peak Down",
															"parameter_steps" : 41,
															"parameter_type" : 0,
															"parameter_unitstyle" : 2
														}

													}
,
													"textcolor" : [ 0.101961, 0.121569, 0.172549, 1.0 ],
													"varname" : "peakdown[3]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-75",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 1018.0, 267.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-74",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1125.0, 540.0, 46.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 168.0, 66.75, 49.0, 48.0 ],
													"prototypename" : "time",
													"saved_attribute_attributes" : 													{
														"textcolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_initial" : [ 300.0 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "peakright[3]",
															"parameter_mmax" : 1000.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Peak Right",
															"parameter_steps" : 41,
															"parameter_type" : 0,
															"parameter_unitstyle" : 2
														}

													}
,
													"textcolor" : [ 0.101961, 0.121569, 0.172549, 1.0 ],
													"varname" : "peakright[3]"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-71",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 960.0, 540.0, 41.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 23.0, 66.75, 41.0, 48.0 ],
													"prototypename" : "pitch",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_initial" : [ 60 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "pitch[3]",
															"parameter_mmax" : 120.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Pitch",
															"parameter_type" : 0,
															"parameter_unitstyle" : 8
														}

													}
,
													"varname" : "pitch[3]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-69",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 472.0, 386.0, 141.0, 22.0 ],
													"text" : "1300., 130. 15 32. 575"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-66",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 958.0, 273.0, 29.5, 22.0 ],
													"text" : "/ 4"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-62",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 813.0, 279.0, 30.0, 22.0 ],
													"text" : "* 10"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-61",
													"maxclass" : "newobj",
													"numinlets" : 5,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 813.0, 333.0, 168.0, 22.0 ],
													"text" : "sprintf %.2f\\, %.2f %d %.2f %d"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-59",
													"maxclass" : "number",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 861.0, 220.0, 50.0, 22.0 ],
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_invisible" : 1,
															"parameter_longname" : "number[8]",
															"parameter_modmode" : 0,
															"parameter_shortname" : "number[1]",
															"parameter_type" : 3
														}

													}
,
													"varname" : "number"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-54",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 653.0, 220.0, 32.0, 22.0 ],
													"text" : "mtof"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-31",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 410.0, 460.0, 84.0, 22.0 ],
													"text" : "r #0-banger"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-30",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 649.0, 297.0, 86.0, 22.0 ],
													"text" : "s #0-banger"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"format" : 6,
													"id" : "obj-29",
													"maxclass" : "flonum",
													"maximum" : 1.0,
													"minimum" : 0.0,
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 503.0, 545.0, 50.0, 22.0 ],
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_longname" : "number[9]",
															"parameter_mmax" : 1.0,
															"parameter_modmode" : 3,
															"parameter_shortname" : "number",
															"parameter_type" : 0
														}

													}
,
													"varname" : "gain"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-28",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 503.0, 626.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-27",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 503.0, 578.0, 60.0, 22.0 ],
													"text" : "pak 0. 50"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-25",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 175.0, 614.0, 347.5, 22.0 ],
													"text" : "*~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-24",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 315.0, 450.0, 45.0, 22.0 ],
													"text" : "cycle~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-22",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 315.0, 410.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-23",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 315.0, 363.0, 86.0, 22.0 ],
													"text" : "r #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-21",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 144.0, 485.0, 189.5, 22.0 ],
													"text" : "+~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-20",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 189.0, 382.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-18",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 189.0, 346.0, 86.0, 22.0 ],
													"text" : "r #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-17",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 186.0, 422.0, 42.0, 22.0 ],
													"text" : "*~ 1.5"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-16",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 824.0, 518.0, 88.0, 22.0 ],
													"text" : "s #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-15",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 145.0, 459.0, 60.0, 22.0 ],
													"text" : "onepole~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-14",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 148.0, 315.0, 189.5, 22.0 ],
													"text" : "+~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-13",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 318.0, 264.0, 46.0, 22.0 ],
													"text" : "noise~"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-12",
													"maxclass" : "button",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 472.0, 312.0, 30.0, 30.0 ],
													"prototypename" : "big",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_enum" : [ "off", "on" ],
															"parameter_longname" : "button[4]",
															"parameter_mmax" : 1,
															"parameter_modmode" : 0,
															"parameter_shortname" : "button",
															"parameter_type" : 2
														}

													}
,
													"varname" : "button"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-9",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 144.0, 543.0, 234.5, 22.0 ],
													"text" : "*~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-8",
													"maxclass" : "newobj",
													"numinlets" : 3,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 148.0, 275.0, 46.0, 22.0 ],
													"text" : "rect~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-7",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 410.0, 555.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-6",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 410.0, 502.0, 117.0, 22.0 ],
													"text" : "0.5, 1 1 0.5 6 0. 260"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-1",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 148.0, 156.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"border" : 2,
													"id" : "obj-81",
													"maxclass" : "panel",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 945.0, 425.0, 256.000006437301636, 182.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 15.0, 21.5, 390.0, 105.0 ],
													"style" : "rnbolight"
												}

											}
, 											{
												"box" : 												{
													"angle" : 270.0,
													"grad1" : [ 0.117647058823529, 0.117647058823529, 0.117647058823529, 1.0 ],
													"grad2" : [ 0.07843137254902, 0.07843137254902, 0.07843137254902, 1.0 ],
													"id" : "obj-4",
													"maxclass" : "panel",
													"mode" : 1,
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 450.0, 435.0, 128.0, 128.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 0.0, 420.0, 150.0 ],
													"proportion" : 0.5,
													"varname" : "backgroundPanel"
												}

											}
, 											{
												"box" : 												{
													"background" : 1,
													"id" : "obj-10",
													"ignoreclick" : 1,
													"maxclass" : "mira.frame",
													"numinlets" : 0,
													"numoutlets" : 0,
													"patching_rect" : [ 945.0, 425.0, 256.000006437301636, 182.0 ]
												}

											}
 ],
										"lines" : [ 											{
												"patchline" : 												{
													"destination" : [ "obj-8", 0 ],
													"source" : [ "obj-1", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-30", 0 ],
													"order" : 0,
													"source" : [ "obj-12", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-69", 0 ],
													"order" : 1,
													"source" : [ "obj-12", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-14", 1 ],
													"source" : [ "obj-13", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-15", 0 ],
													"source" : [ "obj-14", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-21", 0 ],
													"source" : [ "obj-15", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-15", 1 ],
													"source" : [ "obj-17", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-20", 0 ],
													"source" : [ "obj-18", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-17", 0 ],
													"source" : [ "obj-20", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-9", 0 ],
													"source" : [ "obj-21", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-24", 0 ],
													"source" : [ "obj-22", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-22", 0 ],
													"source" : [ "obj-23", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-21", 1 ],
													"source" : [ "obj-24", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-2", 0 ],
													"source" : [ "obj-25", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-28", 0 ],
													"source" : [ "obj-27", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-25", 1 ],
													"source" : [ "obj-28", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-27", 0 ],
													"source" : [ "obj-29", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-12", 0 ],
													"order" : 1,
													"source" : [ "obj-3", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-45", 1 ],
													"order" : 0,
													"source" : [ "obj-3", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-6", 0 ],
													"source" : [ "obj-31", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-40", 0 ],
													"source" : [ "obj-33", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-37", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-38", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-45", 0 ],
													"source" : [ "obj-39", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-36", 0 ],
													"source" : [ "obj-40", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-43", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-47", 0 ],
													"source" : [ "obj-45", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-46", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-46", 0 ],
													"source" : [ "obj-47", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-59", 0 ],
													"source" : [ "obj-54", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 1 ],
													"order" : 1,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 0 ],
													"order" : 2,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-66", 0 ],
													"order" : 0,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-7", 0 ],
													"source" : [ "obj-6", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-69", 1 ],
													"source" : [ "obj-61", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-62", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 3 ],
													"source" : [ "obj-66", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-1", 0 ],
													"order" : 1,
													"source" : [ "obj-69", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-16", 0 ],
													"order" : 0,
													"source" : [ "obj-69", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-9", 1 ],
													"midpoints" : [ 419.5, 515.0, 369.0, 515.0 ],
													"source" : [ "obj-7", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-54", 0 ],
													"source" : [ "obj-71", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-75", 0 ],
													"source" : [ "obj-74", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 4 ],
													"source" : [ "obj-75", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-75", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-78", 0 ],
													"source" : [ "obj-77", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 2 ],
													"source" : [ "obj-78", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-78", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-80", 0 ],
													"source" : [ "obj-79", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-14", 0 ],
													"source" : [ "obj-8", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 1 ],
													"source" : [ "obj-80", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 0 ],
													"source" : [ "obj-80", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-25", 0 ],
													"source" : [ "obj-9", 0 ]
												}

											}
 ],
										"styles" : [ 											{
												"name" : "rnbodefault",
												"default" : 												{
													"accentcolor" : [ 0.343034118413925, 0.506230533123016, 0.86220508813858, 1.0 ],
													"bgcolor" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
													"bgfillcolor" : 													{
														"angle" : 270.0,
														"autogradient" : 0.0,
														"color" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color1" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color2" : [ 0.263682, 0.004541, 0.038797, 1.0 ],
														"proportion" : 0.39,
														"type" : "color"
													}
,
													"color" : [ 0.929412, 0.929412, 0.352941, 1.0 ],
													"elementcolor" : [ 0.357540726661682, 0.515565991401672, 0.861786782741547, 1.0 ],
													"fontname" : [ "Lato" ],
													"fontsize" : [ 12.0 ],
													"stripecolor" : [ 0.258338063955307, 0.352425158023834, 0.511919498443604, 1.0 ],
													"textcolor_inverse" : [ 0.968627, 0.968627, 0.968627, 1 ]
												}
,
												"parentstyle" : "",
												"multi" : 0
											}
, 											{
												"name" : "rnbolight",
												"default" : 												{
													"accentcolor" : [ 0.443137254901961, 0.505882352941176, 0.556862745098039, 1.0 ],
													"bgcolor" : [ 0.796078431372549, 0.862745098039216, 0.925490196078431, 1.0 ],
													"bgfillcolor" : 													{
														"angle" : 270.0,
														"autogradient" : 0.0,
														"color" : [ 0.835294117647059, 0.901960784313726, 0.964705882352941, 1.0 ],
														"color1" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color2" : [ 0.263682, 0.004541, 0.038797, 1.0 ],
														"proportion" : 0.39,
														"type" : "color"
													}
,
													"clearcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"color" : [ 0.815686274509804, 0.509803921568627, 0.262745098039216, 1.0 ],
													"editing_bgcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"elementcolor" : [ 0.337254901960784, 0.384313725490196, 0.462745098039216, 1.0 ],
													"fontname" : [ "Lato" ],
													"locked_bgcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"stripecolor" : [ 0.309803921568627, 0.698039215686274, 0.764705882352941, 1.0 ],
													"textcolor_inverse" : [ 0.0, 0.0, 0.0, 1.0 ]
												}
,
												"parentstyle" : "",
												"multi" : 0
											}
 ]
									}
,
									"patching_rect" : [ 248.0, 223.0, 420.0, 150.0 ],
									"varname" : "custom.drum",
									"viewvisibility" : 1
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 1 ],
									"order" : 1,
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-7", 0 ],
									"order" : 0,
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-10", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"source" : [ "obj-15", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-6", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-9", 0 ],
									"source" : [ "obj-7", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"source" : [ "obj-9", 0 ]
								}

							}
 ]
					}
,
					"patching_rect" : [ 731.0, 198.0, 39.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"globalpatchername" : "",
						"tags" : ""
					}
,
					"text" : "p tom",
					"varname" : "tom[1]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-18",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 6,
							"revision" : 5,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 0.0, 26.0, 975.0, 689.0 ],
						"bglocked" : 0,
						"openinpresentation" : 0,
						"default_fontsize" : 12.0,
						"default_fontface" : 0,
						"default_fontname" : "Arial",
						"gridonopen" : 1,
						"gridsize" : [ 15.0, 15.0 ],
						"gridsnaponopen" : 1,
						"objectsnaponopen" : 1,
						"statusbarvisible" : 2,
						"toolbarvisible" : 1,
						"lefttoolbarpinned" : 0,
						"toptoolbarpinned" : 0,
						"righttoolbarpinned" : 0,
						"bottomtoolbarpinned" : 0,
						"toolbars_unpinned_last_save" : 0,
						"tallnewobj" : 0,
						"boxanimatetime" : 200,
						"enablehscroll" : 1,
						"enablevscroll" : 1,
						"devicewidth" : 0.0,
						"description" : "",
						"digest" : "",
						"tags" : "",
						"style" : "",
						"subpatcher_template" : "",
						"showontab" : 1,
						"assistshowspatchername" : 0,
						"boxes" : [ 							{
								"box" : 								{
									"id" : "obj-10",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 44.0, 473.0, 34.0, 22.0 ],
									"text" : "limi~"
								}

							}
, 							{
								"box" : 								{
									"autosave" : 1,
									"bgmode" : 0,
									"border" : 0,
									"clickthrough" : 0,
									"id" : "obj-28",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 8,
									"offset" : [ 0.0, 0.0 ],
									"outlettype" : [ "signal", "signal", "", "list", "int", "", "", "" ],
									"patching_rect" : [ 44.0, 528.0, 300.0, 100.0 ],
									"save" : [ "#N", "vst~", "loaduniqueid", 0, "C74_AU:/kHs Compressor", ";" ],
									"saved_attribute_attributes" : 									{
										"valueof" : 										{
											"parameter_invisible" : 1,
											"parameter_longname" : "vst~",
											"parameter_modmode" : 0,
											"parameter_shortname" : "vst~",
											"parameter_type" : 3
										}

									}
,
									"saved_object_attributes" : 									{
										"parameter_enable" : 1,
										"parameter_mappable" : 0
									}
,
									"snapshot" : 									{
										"filetype" : "C74Snapshot",
										"version" : 2,
										"minorversion" : 0,
										"name" : "snapshotlist",
										"origin" : "vst~",
										"type" : "list",
										"subtype" : "Undefined",
										"embed" : 1,
										"snapshot" : 										{
											"pluginname" : "kHs Compressor.auinfo",
											"plugindisplayname" : "kHs Compressor",
											"pluginsavedname" : "C74_AU:/kHs Compressor",
											"pluginsaveduniqueid" : 711806331,
											"version" : 1,
											"isbank" : 0,
											"isbase64" : 1,
											"sliderorder" : [  ],
											"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
											"blob" : "803.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBbHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HaByEAtjfz.+tGtHY6r7H7ew.Z9IG9Q5yyKymwz1NRw9wcuLe1LVG0yipfe76YruDddfRecM4qk5CbGYB6O3rwgb7xw5jg+fh5xkBtHMVUKMRs7+058bkeJH5o8J6S6GbjP5kVS5qCRw9mrtS7TuMeXGJofLkcINcMKEcNmy7xNRbjKMWtAxRKLVyTGLbc4F8699wJWtjRyPLr2qrgqc7RnvpSL8dqqrM1Ak8gzg+wmpofw6tsKp3gzcKuz+lqMqrga2x0EU2UJKvcGnPt6mmJ8oOto5hn6Q5l+ERk35ziW3s071nSPkNVpL1WfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.lOES92+URYln9WuYd4R6a9zj3o4mnwoMbQy5cqZ2sszTV3ni7GsptwrkqZW1zrqF5x8JGztXYy5Ms22Vqmm6wb4AheZbkjh395MHs1llu2ztYUMiGB75.Glitey5Maa2lnkkwxiEX8MJuTpSFd2qCafGNlqzyEAq64u8SWT6u6OQi33hSdwPcUSSl3MoSGwijKOdjSmguqXoccci8VmlWdlaFOOU7PYFHYMK2zN0DME3028yyeEPszAHDjs6bY.B...6mC...0RAH...PA.Hf.B.vihhqUP1tykAH...reN..fB......................vbzEFck4hZy8laPsTAF.....P..D..3....ji......HQX0YFdRr1biAGDA..B.TA.Z.vI.vB.w.PN.DD.MAfTBzs.hKv4........BD..........M...................BjN"
										}
,
										"snapshotlist" : 										{
											"current_snapshot" : 0,
											"entries" : [ 												{
													"filetype" : "C74Snapshot",
													"version" : 2,
													"minorversion" : 0,
													"name" : "kHs Compressor",
													"origin" : "kHs Compressor.auinfo",
													"type" : "AudioUnit",
													"subtype" : "AudioEffect",
													"embed" : 0,
													"snapshot" : 													{
														"pluginname" : "kHs Compressor.auinfo",
														"plugindisplayname" : "kHs Compressor",
														"pluginsavedname" : "C74_AU:/kHs Compressor",
														"pluginsaveduniqueid" : 711806331,
														"version" : 1,
														"isbank" : 0,
														"isbase64" : 1,
														"sliderorder" : [  ],
														"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
														"blob" : "803.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBbHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HaByEAtjfz.+tGtHY6r7H7ew.Z9IG9Q5yyKymwz1NRw9wcuLe1LVG0yipfe76YruDddfRecM4qk5CbGYB6O3rwgb7xw5jg+fh5xkBtHMVUKMRs7+058bkeJH5o8J6S6GbjP5kVS5qCRw9mrtS7TuMeXGJofLkcINcMKEcNmy7xNRbjKMWtAxRKLVyTGLbc4F8699wJWtjRyPLr2qrgqc7RnvpSL8dqqrM1Ak8gzg+wmpofw6tsKp3gzcKuz+lqMqrga2x0EU2UJKvcGnPt6mmJ8oOto5hn6Q5l+ERk35ziW3s071nSPkNVpL1WfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.lOES92+URYln9WuYd4R6a9zj3o4mnwoMbQy5cqZ2sszTV3ni7GsptwrkqZW1zrqF5x8JGztXYy5Ms22Vqmm6wb4AheZbkjh395MHs1llu2ztYUMiGB75.Glitey5Maa2lnkkwxiEX8MJuTpSFd2qCafGNlqzyEAq64u8SWT6u6OQi33hSdwPcUSSl3MoSGwijKOdjSmguqXoccci8VmlWdlaFOOU7PYFHYMK2zN0DME3028yyeEPszAHDjs6bY.B...6mC...0RAH...PA.Hf.B.vihhqUP1tykAH...reN..fB......................vbzEFck4hZy8laPsTAF.....P..D..3....ji......HQX0YFdRr1biAGDA..B.TA.Z.vI.vB.w.PN.DD.MAfTBzs.hKv4........BD..........M...................BjN"
													}
,
													"fileref" : 													{
														"name" : "kHs Compressor",
														"filename" : "kHs Compressor.maxsnap",
														"filepath" : "~/Documents/Max 8/Projects/Resonance/data",
														"filepos" : -1,
														"snapshotfileid" : "99cabb973ac56104aab1d2c762bb18cb"
													}

												}
 ]
										}

									}
,
									"text" : "vst~ \"C74_AU:/kHs Compressor\"",
									"varname" : "vst~",
									"viewvisibility" : 1
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-8",
									"maxclass" : "button",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 214.0, 9.0, 24.0, 24.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "preset",
									"numinlets" : 1,
									"numoutlets" : 5,
									"outlettype" : [ "preset", "int", "preset", "int", "" ],
									"patching_rect" : [ 550.0, 134.0, 100.0, 40.0 ],
									"preset_data" : [ 										{
											"number" : 1,
											"data" : [ 5, "obj-6", "flonum", "float", 40.0, 5, "<invalid>", "flonum", "float", 881.0, 6, "obj-23", "gain~", "list", 96, 10.0 ]
										}
, 										{
											"number" : 2,
											"data" : [ 5, "obj-6", "flonum", "float", 1.820000052452087, 5, "<invalid>", "flonum", "float", 673.0, 6, "obj-23", "gain~", "list", 27, 10.0 ]
										}
, 										{
											"number" : 3,
											"data" : [ 5, "obj-6", "flonum", "float", 9.0, 5, "<invalid>", "flonum", "float", 881.0, 6, "obj-23", "gain~", "list", 96, 10.0 ]
										}
 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-23",
									"maxclass" : "gain~",
									"multichannelvariant" : 0,
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "signal", "" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 242.0, 299.0, 22.0, 140.0 ]
								}

							}
, 							{
								"box" : 								{
									"format" : 6,
									"id" : "obj-22",
									"maxclass" : "flonum",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "bang" ],
									"parameter_enable" : 1,
									"patching_rect" : [ 298.0, 213.0, 50.0, 22.0 ],
									"saved_attribute_attributes" : 									{
										"valueof" : 										{
											"parameter_invisible" : 1,
											"parameter_longname" : "number[10]",
											"parameter_modmode" : 0,
											"parameter_shortname" : "number[10]",
											"parameter_type" : 3
										}

									}
,
									"varname" : "reverb"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-14",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 242.0, 254.0, 75.0, 22.0 ],
									"text" : "cverb~ 1000"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-13",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 550.0, 65.0, 135.0, 22.0 ],
									"saved_object_attributes" : 									{
										"client_rect" : [ 580, 87, 949, 304 ],
										"parameter_enable" : 0,
										"parameter_mappable" : 0,
										"storage_rect" : [ 583, 69, 1034, 197 ]
									}
,
									"text" : "pattrstorage @greedy 1",
									"varname" : "u856003620"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-11",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 4,
									"outlettype" : [ "", "", "", "" ],
									"patching_rect" : [ 550.0, 100.0, 56.0, 22.0 ],
									"restore" : 									{
										"overdrive" : [ 2.3 ],
										"reverb" : [ 2327.0 ],
										"vst~" : [ 											{
												"filetype" : "C74Snapshot",
												"version" : 2,
												"minorversion" : 0,
												"name" : "kHs Compressor",
												"origin" : "kHs Compressor.auinfo",
												"type" : "AudioUnit",
												"subtype" : "AudioEffect",
												"embed" : 1,
												"snapshot" : 												{
													"pluginname" : "kHs Compressor.auinfo",
													"plugindisplayname" : "kHs Compressor",
													"pluginsavedname" : "C74_AU:/kHs Compressor",
													"pluginsaveduniqueid" : 711806331,
													"version" : 1,
													"isbank" : 0,
													"isbase64" : 1,
													"sliderorder" : [  ],
													"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
													"blob" : "803.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBbHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HaByEAtjfz.+tGtHY6r7H7ew.Z9IG9Q5yyKymwz1NRw9wcuLe1LVG0yipfe76YruDddfRecM4qk5CbGYB6O3rwgb7xw5jg+fh5xkBtHMVUKMRs7+058bkeJH5o8J6S6GbjP5kVS5qCRw9mrtS7TuMeXGJofLkcINcMKEcNmy7xNRbjKMWtAxRKLVyTGLbc4F8699wJWtjRyPLr2qrgqc7RnvpSL8dqqrM1Ak8gzg+wmpofw6tsKp3gzcKuz+lqMqrga2x0EU2UJKvcGnPt6mmJ8oOto5hn6Q5l+ERk35ziW3s071nSPkNVpL1WfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.lOES92+URYln9WuYd4R6a9zj3o4mnwoMbQy5cqZ2sszTV3ni7GsptwrkqZW1zrqF5x8JGztXYy5Ms22Vqmm6wb4AheZbkjh395MHs1llu2ztYUMiGB75.Glitey5Maa2lnkkwxiEX8MJuTpSFd2qCafGNlqzyEAq64u8SWT6u6OQi33hSdwPcUSSl3MoSGwijKOdjSmguqXoccci8VmlWdlaFOOU7PYFHYMK2zN0DME3028yyeEPszAHDjs6bY.B...6mC...0RAH...PA.Hf.B.vihhqUP1tykAH...reN..fB......................vbzEFck4hZy8laPsTAF.....P..D..3....ji......HQX0YFdRr1biAGDA..B.TA.Z.vI.vB.w.PN.DD.MAfTBzs.hKv4........BD..........M...................BjN"
												}

											}
 ]
									}
,
									"text" : "autopattr",
									"varname" : "u028002892"
								}

							}
, 							{
								"box" : 								{
									"format" : 6,
									"id" : "obj-6",
									"maxclass" : "flonum",
									"minimum" : 0.01,
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "bang" ],
									"parameter_enable" : 1,
									"patching_rect" : [ 175.0, 254.0, 50.0, 22.0 ],
									"saved_attribute_attributes" : 									{
										"valueof" : 										{
											"parameter_invisible" : 1,
											"parameter_longname" : "number",
											"parameter_mmin" : 0.01,
											"parameter_modmode" : 0,
											"parameter_shortname" : "number",
											"parameter_type" : 3
										}

									}
,
									"varname" : "overdrive"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-4",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 129.0, 307.0, 65.0, 22.0 ],
									"text" : "overdrive~"
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-3",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 44.0, 654.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-1",
									"maxclass" : "newobj",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 42.0, 10.0, 36.0, 22.0 ],
									"text" : "r kick"
								}

							}
, 							{
								"box" : 								{
									"bgmode" : 0,
									"border" : 0,
									"clickthrough" : 0,
									"embed" : 1,
									"enablehscroll" : 0,
									"enablevscroll" : 0,
									"id" : "obj-2",
									"lockeddragscroll" : 0,
									"lockedsize" : 0,
									"maxclass" : "bpatcher",
									"name" : "custom.drum.maxpat",
									"numinlets" : 2,
									"numoutlets" : 1,
									"offset" : [ 0.0, 0.0 ],
									"outlettype" : [ "signal" ],
									"patcher" : 									{
										"fileversion" : 1,
										"appversion" : 										{
											"major" : 8,
											"minor" : 6,
											"revision" : 5,
											"architecture" : "x64",
											"modernui" : 1
										}
,
										"classnamespace" : "box",
										"rect" : [ 47.0, 87.0, 683.0, 701.0 ],
										"bglocked" : 0,
										"openinpresentation" : 1,
										"default_fontsize" : 12.0,
										"default_fontface" : 0,
										"default_fontname" : "Arial",
										"gridonopen" : 1,
										"gridsize" : [ 15.0, 15.0 ],
										"gridsnaponopen" : 2,
										"objectsnaponopen" : 1,
										"statusbarvisible" : 2,
										"toolbarvisible" : 1,
										"lefttoolbarpinned" : 0,
										"toptoolbarpinned" : 0,
										"righttoolbarpinned" : 0,
										"bottomtoolbarpinned" : 0,
										"toolbars_unpinned_last_save" : 0,
										"tallnewobj" : 0,
										"boxanimatetime" : 200,
										"enablehscroll" : 1,
										"enablevscroll" : 1,
										"devicewidth" : 0.0,
										"description" : "",
										"digest" : "",
										"tags" : "",
										"style" : "",
										"subpatcher_template" : "<none>",
										"assistshowspatchername" : 0,
										"boxes" : [ 											{
												"box" : 												{
													"id" : "obj-40",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 227.0, 54.0, 22.0 ],
													"text" : "deferlow"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-36",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 297.0, 65.0, 22.0 ],
													"saved_object_attributes" : 													{
														"filename" : "resize.js",
														"parameter_enable" : 0
													}
,
													"text" : "js resize.js"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-33",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1095.0, 195.0, 95.0, 22.0 ],
													"text" : "loadmess resize"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-11",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "" ],
													"patching_rect" : [ 675.0, 615.0, 67.0, 22.0 ],
													"save" : [ "#N", "thispatcher", ";", "#Q", "end", ";" ],
													"text" : "thispatcher"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-45",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1010.75, 87.0, 32.0, 22.0 ],
													"text" : "gate"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-46",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 1010.75, 156.0, 29.5, 22.0 ],
													"text" : "+ 1"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-47",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 1010.75, 120.0, 66.0, 22.0 ],
													"text" : "random 16"
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-43",
													"index" : 2,
													"maxclass" : "inlet",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 957.75, 142.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-42",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 270.0, 330.0, 148.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 143.0, 36.25, 74.0, 21.0 ],
													"text" : "Randomize"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-39",
													"maxclass" : "live.toggle",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1010.75, 52.5, 15.0, 15.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 219.0, 37.125, 19.0, 19.25 ],
													"saved_attribute_attributes" : 													{
														"activebgoncolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_enum" : [ "off", "on" ],
															"parameter_longname" : "live.toggle[4]",
															"parameter_mmax" : 1,
															"parameter_modmode" : 0,
															"parameter_shortname" : "live.toggle",
															"parameter_type" : 2
														}

													}
,
													"varname" : "randomize"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 13.0,
													"id" : "obj-38",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 791.5, 14.5, 196.0, 23.0 ],
													"text" : "pattrstorage presetPattrstorage"
												}

											}
, 											{
												"box" : 												{
													"attr" : "bubblesize",
													"id" : "obj-37",
													"maxclass" : "attrui",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"parameter_enable" : 0,
													"patching_rect" : [ 615.0, 15.0, 150.0, 22.0 ]
												}

											}
, 											{
												"box" : 												{
													"active1" : [ 1.0, 0.709803921568627, 0.196078431372549, 1.0 ],
													"bubblesize" : 14,
													"id" : "obj-35",
													"maxclass" : "preset",
													"numinlets" : 1,
													"numoutlets" : 5,
													"outlettype" : [ "preset", "int", "preset", "int", "" ],
													"patching_rect" : [ 615.0, 146.0, 100.0, 40.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 246.0, 36.25, 150.0, 77.5 ],
													"preset_data" : [ 														{
															"number" : 1,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 48, 5, "obj-71", "live.dial", "float", 31.0, 5, "obj-74", "live.dial", "float", 200.0, 5, "obj-77", "live.dial", "float", 20.0, 5, "obj-79", "live.dial", "float", 6.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
, 														{
															"number" : 2,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 61, 5, "obj-71", "live.dial", "float", 35.0, 5, "obj-74", "live.dial", "float", 125.0, 5, "obj-77", "live.dial", "float", 17.5, 5, "obj-79", "live.dial", "float", 7.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
, 														{
															"number" : 3,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 77, 5, "obj-71", "live.dial", "float", 39.0, 5, "obj-74", "live.dial", "float", 275.0, 5, "obj-77", "live.dial", "float", 20.0, 5, "obj-79", "live.dial", "float", 7.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
, 														{
															"number" : 4,
															"data" : [ 5, "obj-29", "flonum", "float", 1.0, 5, "obj-59", "number", "int", 61, 5, "obj-71", "live.dial", "float", 35.0, 5, "obj-74", "live.dial", "float", 275.0, 5, "obj-77", "live.dial", "float", 17.5, 5, "obj-79", "live.dial", "float", 7.0, 5, "obj-37", "attrui", "attr", "bubblesize", 5, "obj-37", "attrui", "int", 14, 5, "obj-39", "live.toggle", "float", 0.0 ]
														}
 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-34",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 204.0, 180.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 129.0, 60.0, 21.0 ],
													"text" : "Output",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-32",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 240.0, 135.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 339.0, 0.0, 81.0, 21.0 ],
													"text" : "Select Preset",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-19",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 285.0, 195.0, 160.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 0.0, 64.0, 21.0 ],
													"text" : "Trigger",
													"textcolor" : [ 1.0, 1.0, 1.0, 1.0 ]
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-3",
													"index" : 1,
													"maxclass" : "inlet",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "bang" ],
													"patching_rect" : [ 390.0, 45.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-26",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 4,
													"outlettype" : [ "", "", "", "" ],
													"patching_rect" : [ 525.0, 146.0, 56.0, 22.0 ],
													"restore" : 													{
														"button" : [ 1.0 ],
														"gain" : [ 1.0 ],
														"number" : [ 77 ],
														"peakdown[2]" : [ 20.0 ],
														"peakright[2]" : [ 275.0 ],
														"pitch[2]" : [ 39.0 ],
														"randomize" : [ 0.0 ],
														"snap[1]" : [ 7.0 ]
													}
,
													"text" : "autopattr",
													"varname" : "u477009426"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-5",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 390.0, 161.0, 103.0, 22.0 ],
													"saved_object_attributes" : 													{
														"client_rect" : [ 580, 87, 949, 304 ],
														"parameter_enable" : 0,
														"parameter_mappable" : 0,
														"storage_rect" : [ 583, 69, 1034, 197 ]
													}
,
													"text" : "pattrstorage drum",
													"varname" : "drum"
												}

											}
, 											{
												"box" : 												{
													"comment" : "",
													"id" : "obj-2",
													"index" : 1,
													"maxclass" : "outlet",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 175.0, 660.0, 30.0, 30.0 ]
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-85",
													"maxclass" : "comment",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 957.75, 442.0, 155.0, 21.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 22.0, 29.5, 155.0, 21.0 ],
													"text" : "Drum Generator"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-80",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 808.0, 227.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-79",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1010.75, 540.0, 45.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 66.0, 66.75, 44.0, 48.0 ],
													"prototypename" : "gain",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_initial" : [ 10 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "snap[1]",
															"parameter_mmax" : 20.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Snap",
															"parameter_steps" : 21,
															"parameter_type" : 1,
															"parameter_unitstyle" : 0
														}

													}
,
													"varname" : "snap[1]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-78",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 915.0, 282.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-77",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1056.75, 540.0, 57.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 116.0, 66.75, 49.0, 48.0 ],
													"prototypename" : "time",
													"saved_attribute_attributes" : 													{
														"textcolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_initial" : [ 10.0 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "peakdown[2]",
															"parameter_mmax" : 50.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Peak Down",
															"parameter_steps" : 41,
															"parameter_type" : 0,
															"parameter_unitstyle" : 2
														}

													}
,
													"textcolor" : [ 0.101961, 0.121569, 0.172549, 1.0 ],
													"varname" : "peakdown[2]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-75",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "bang", "int" ],
													"patching_rect" : [ 1018.0, 267.0, 29.5, 22.0 ],
													"text" : "t b i"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-74",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 1125.0, 540.0, 46.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 168.0, 66.75, 49.0, 48.0 ],
													"prototypename" : "time",
													"saved_attribute_attributes" : 													{
														"textcolor" : 														{
															"expression" : ""
														}
,
														"valueof" : 														{
															"parameter_initial" : [ 300.0 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "peakright[2]",
															"parameter_mmax" : 1000.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Peak Right",
															"parameter_steps" : 41,
															"parameter_type" : 0,
															"parameter_unitstyle" : 2
														}

													}
,
													"textcolor" : [ 0.101961, 0.121569, 0.172549, 1.0 ],
													"varname" : "peakright[2]"
												}

											}
, 											{
												"box" : 												{
													"annotation" : "",
													"fontname" : "Ableton Sans Bold",
													"id" : "obj-71",
													"maxclass" : "live.dial",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "float" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 960.0, 540.0, 41.0, 48.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 23.0, 66.75, 41.0, 48.0 ],
													"prototypename" : "pitch",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_initial" : [ 60 ],
															"parameter_initial_enable" : 1,
															"parameter_linknames" : 1,
															"parameter_longname" : "pitch[2]",
															"parameter_mmax" : 120.0,
															"parameter_modmode" : 0,
															"parameter_shortname" : "Pitch",
															"parameter_type" : 0,
															"parameter_unitstyle" : 8
														}

													}
,
													"varname" : "pitch[2]"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-69",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 472.0, 386.0, 141.0, 22.0 ],
													"text" : "539., 77. 20 19. 275"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-66",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 958.0, 273.0, 29.5, 22.0 ],
													"text" : "/ 4"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-62",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "int" ],
													"patching_rect" : [ 813.0, 279.0, 30.0, 22.0 ],
													"text" : "* 10"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-61",
													"maxclass" : "newobj",
													"numinlets" : 5,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 813.0, 333.0, 168.0, 22.0 ],
													"text" : "sprintf %.2f\\, %.2f %d %.2f %d"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-59",
													"maxclass" : "number",
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 861.0, 220.0, 50.0, 22.0 ],
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_invisible" : 1,
															"parameter_longname" : "number[6]",
															"parameter_modmode" : 0,
															"parameter_shortname" : "number[1]",
															"parameter_type" : 3
														}

													}
,
													"varname" : "number"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-54",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 653.0, 220.0, 32.0, 22.0 ],
													"text" : "mtof"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-31",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 410.0, 460.0, 84.0, 22.0 ],
													"text" : "r #0-banger"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-30",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 649.0, 297.0, 86.0, 22.0 ],
													"text" : "s #0-banger"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"format" : 6,
													"id" : "obj-29",
													"maxclass" : "flonum",
													"maximum" : 1.0,
													"minimum" : 0.0,
													"numinlets" : 1,
													"numoutlets" : 2,
													"outlettype" : [ "", "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 503.0, 545.0, 50.0, 22.0 ],
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_longname" : "number[7]",
															"parameter_mmax" : 1.0,
															"parameter_modmode" : 3,
															"parameter_shortname" : "number",
															"parameter_type" : 0
														}

													}
,
													"varname" : "gain"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-28",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 503.0, 626.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-27",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 503.0, 578.0, 60.0, 22.0 ],
													"text" : "pak 0. 50"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-25",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 175.0, 614.0, 347.5, 22.0 ],
													"text" : "*~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-24",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 315.0, 450.0, 45.0, 22.0 ],
													"text" : "cycle~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-22",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 315.0, 410.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-23",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 315.0, 363.0, 86.0, 22.0 ],
													"text" : "r #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-21",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 144.0, 485.0, 189.5, 22.0 ],
													"text" : "+~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-20",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 189.0, 382.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-18",
													"maxclass" : "newobj",
													"numinlets" : 0,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 189.0, 346.0, 86.0, 22.0 ],
													"text" : "r #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-17",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 186.0, 422.0, 42.0, 22.0 ],
													"text" : "*~ 1.5"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-16",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 824.0, 518.0, 88.0, 22.0 ],
													"text" : "s #0-freqline"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-15",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 145.0, 459.0, 60.0, 22.0 ],
													"text" : "onepole~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-14",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 148.0, 315.0, 189.5, 22.0 ],
													"text" : "+~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-13",
													"maxclass" : "newobj",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 318.0, 264.0, 46.0, 22.0 ],
													"text" : "noise~"
												}

											}
, 											{
												"box" : 												{
													"id" : "obj-12",
													"maxclass" : "button",
													"numinlets" : 1,
													"numoutlets" : 1,
													"outlettype" : [ "bang" ],
													"parameter_enable" : 1,
													"patching_rect" : [ 472.0, 312.0, 30.0, 30.0 ],
													"prototypename" : "big",
													"saved_attribute_attributes" : 													{
														"valueof" : 														{
															"parameter_enum" : [ "off", "on" ],
															"parameter_longname" : "button[3]",
															"parameter_mmax" : 1,
															"parameter_modmode" : 0,
															"parameter_shortname" : "button",
															"parameter_type" : 2
														}

													}
,
													"varname" : "button"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-9",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 144.0, 543.0, 234.5, 22.0 ],
													"text" : "*~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-8",
													"maxclass" : "newobj",
													"numinlets" : 3,
													"numoutlets" : 1,
													"outlettype" : [ "signal" ],
													"patching_rect" : [ 148.0, 275.0, 46.0, 22.0 ],
													"text" : "rect~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-7",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 410.0, 555.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-6",
													"maxclass" : "message",
													"numinlets" : 2,
													"numoutlets" : 1,
													"outlettype" : [ "" ],
													"patching_rect" : [ 410.0, 502.0, 117.0, 22.0 ],
													"text" : "0.5, 1 1 0.5 6 0. 260"
												}

											}
, 											{
												"box" : 												{
													"fontname" : "Arial",
													"fontsize" : 12.0,
													"id" : "obj-1",
													"maxclass" : "newobj",
													"numinlets" : 2,
													"numoutlets" : 2,
													"outlettype" : [ "signal", "bang" ],
													"patching_rect" : [ 148.0, 156.0, 36.0, 22.0 ],
													"text" : "line~"
												}

											}
, 											{
												"box" : 												{
													"border" : 2,
													"id" : "obj-81",
													"maxclass" : "panel",
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 945.0, 425.0, 256.000006437301636, 182.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 15.0, 21.5, 390.0, 105.0 ],
													"style" : "rnbolight"
												}

											}
, 											{
												"box" : 												{
													"angle" : 270.0,
													"grad1" : [ 0.117647058823529, 0.117647058823529, 0.117647058823529, 1.0 ],
													"grad2" : [ 0.07843137254902, 0.07843137254902, 0.07843137254902, 1.0 ],
													"id" : "obj-4",
													"maxclass" : "panel",
													"mode" : 1,
													"numinlets" : 1,
													"numoutlets" : 0,
													"patching_rect" : [ 450.0, 435.0, 128.0, 128.0 ],
													"presentation" : 1,
													"presentation_rect" : [ 0.0, 0.0, 420.0, 150.0 ],
													"proportion" : 0.5,
													"varname" : "backgroundPanel"
												}

											}
, 											{
												"box" : 												{
													"background" : 1,
													"id" : "obj-10",
													"ignoreclick" : 1,
													"maxclass" : "mira.frame",
													"numinlets" : 0,
													"numoutlets" : 0,
													"patching_rect" : [ 945.0, 425.0, 256.000006437301636, 182.0 ]
												}

											}
 ],
										"lines" : [ 											{
												"patchline" : 												{
													"destination" : [ "obj-8", 0 ],
													"source" : [ "obj-1", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-30", 0 ],
													"order" : 0,
													"source" : [ "obj-12", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-69", 0 ],
													"order" : 1,
													"source" : [ "obj-12", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-14", 1 ],
													"source" : [ "obj-13", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-15", 0 ],
													"source" : [ "obj-14", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-21", 0 ],
													"source" : [ "obj-15", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-15", 1 ],
													"source" : [ "obj-17", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-20", 0 ],
													"source" : [ "obj-18", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-17", 0 ],
													"source" : [ "obj-20", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-9", 0 ],
													"source" : [ "obj-21", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-24", 0 ],
													"source" : [ "obj-22", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-22", 0 ],
													"source" : [ "obj-23", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-21", 1 ],
													"source" : [ "obj-24", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-2", 0 ],
													"source" : [ "obj-25", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-28", 0 ],
													"source" : [ "obj-27", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-25", 1 ],
													"source" : [ "obj-28", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-27", 0 ],
													"source" : [ "obj-29", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-12", 0 ],
													"order" : 1,
													"source" : [ "obj-3", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-45", 1 ],
													"order" : 0,
													"source" : [ "obj-3", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-6", 0 ],
													"source" : [ "obj-31", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-40", 0 ],
													"source" : [ "obj-33", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-37", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-38", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-45", 0 ],
													"source" : [ "obj-39", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-36", 0 ],
													"source" : [ "obj-40", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-43", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-47", 0 ],
													"source" : [ "obj-45", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-35", 0 ],
													"source" : [ "obj-46", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-46", 0 ],
													"source" : [ "obj-47", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-59", 0 ],
													"source" : [ "obj-54", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 1 ],
													"order" : 1,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 0 ],
													"order" : 2,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-66", 0 ],
													"order" : 0,
													"source" : [ "obj-59", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-7", 0 ],
													"source" : [ "obj-6", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-69", 1 ],
													"source" : [ "obj-61", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-62", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 3 ],
													"source" : [ "obj-66", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-1", 0 ],
													"order" : 1,
													"source" : [ "obj-69", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-16", 0 ],
													"order" : 0,
													"source" : [ "obj-69", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-9", 1 ],
													"midpoints" : [ 419.5, 585.0, 369.0, 585.0 ],
													"source" : [ "obj-7", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-54", 0 ],
													"source" : [ "obj-71", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-75", 0 ],
													"source" : [ "obj-74", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 4 ],
													"source" : [ "obj-75", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-75", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-78", 0 ],
													"source" : [ "obj-77", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 2 ],
													"source" : [ "obj-78", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-61", 0 ],
													"source" : [ "obj-78", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-80", 0 ],
													"source" : [ "obj-79", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-14", 0 ],
													"source" : [ "obj-8", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 1 ],
													"source" : [ "obj-80", 1 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-62", 0 ],
													"source" : [ "obj-80", 0 ]
												}

											}
, 											{
												"patchline" : 												{
													"destination" : [ "obj-25", 0 ],
													"source" : [ "obj-9", 0 ]
												}

											}
 ],
										"styles" : [ 											{
												"name" : "rnbodefault",
												"default" : 												{
													"accentcolor" : [ 0.343034118413925, 0.506230533123016, 0.86220508813858, 1.0 ],
													"bgcolor" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
													"bgfillcolor" : 													{
														"angle" : 270.0,
														"autogradient" : 0.0,
														"color" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color1" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color2" : [ 0.263682, 0.004541, 0.038797, 1.0 ],
														"proportion" : 0.39,
														"type" : "color"
													}
,
													"color" : [ 0.929412, 0.929412, 0.352941, 1.0 ],
													"elementcolor" : [ 0.357540726661682, 0.515565991401672, 0.861786782741547, 1.0 ],
													"fontname" : [ "Lato" ],
													"fontsize" : [ 12.0 ],
													"stripecolor" : [ 0.258338063955307, 0.352425158023834, 0.511919498443604, 1.0 ],
													"textcolor_inverse" : [ 0.968627, 0.968627, 0.968627, 1 ]
												}
,
												"parentstyle" : "",
												"multi" : 0
											}
, 											{
												"name" : "rnbolight",
												"default" : 												{
													"accentcolor" : [ 0.443137254901961, 0.505882352941176, 0.556862745098039, 1.0 ],
													"bgcolor" : [ 0.796078431372549, 0.862745098039216, 0.925490196078431, 1.0 ],
													"bgfillcolor" : 													{
														"angle" : 270.0,
														"autogradient" : 0.0,
														"color" : [ 0.835294117647059, 0.901960784313726, 0.964705882352941, 1.0 ],
														"color1" : [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
														"color2" : [ 0.263682, 0.004541, 0.038797, 1.0 ],
														"proportion" : 0.39,
														"type" : "color"
													}
,
													"clearcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"color" : [ 0.815686274509804, 0.509803921568627, 0.262745098039216, 1.0 ],
													"editing_bgcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"elementcolor" : [ 0.337254901960784, 0.384313725490196, 0.462745098039216, 1.0 ],
													"fontname" : [ "Lato" ],
													"locked_bgcolor" : [ 0.898039, 0.898039, 0.898039, 1.0 ],
													"stripecolor" : [ 0.309803921568627, 0.698039215686274, 0.764705882352941, 1.0 ],
													"textcolor_inverse" : [ 0.0, 0.0, 0.0, 1.0 ]
												}
,
												"parentstyle" : "",
												"multi" : 0
											}
 ]
									}
,
									"patching_rect" : [ 42.0, 54.0, 420.0, 150.0 ],
									"varname" : "custom.drum",
									"viewvisibility" : 1
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-28", 0 ],
									"source" : [ "obj-10", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-23", 0 ],
									"source" : [ "obj-14", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"order" : 2,
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-14", 0 ],
									"order" : 0,
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 0 ],
									"order" : 1,
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-14", 1 ],
									"source" : [ "obj-22", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"source" : [ "obj-23", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"source" : [ "obj-28", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"source" : [ "obj-28", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-10", 0 ],
									"source" : [ "obj-4", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 1 ],
									"source" : [ "obj-6", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-2", 0 ],
									"source" : [ "obj-8", 0 ]
								}

							}
 ]
					}
,
					"patching_rect" : [ 669.0, 198.0, 39.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"globalpatchername" : "",
						"tags" : ""
					}
,
					"text" : "p kick",
					"varname" : "kick[1]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-16",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 6,
							"revision" : 5,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 0.0, 26.0, 975.0, 689.0 ],
						"bglocked" : 0,
						"openinpresentation" : 0,
						"default_fontsize" : 12.0,
						"default_fontface" : 0,
						"default_fontname" : "Arial",
						"gridonopen" : 1,
						"gridsize" : [ 15.0, 15.0 ],
						"gridsnaponopen" : 1,
						"objectsnaponopen" : 1,
						"statusbarvisible" : 2,
						"toolbarvisible" : 1,
						"lefttoolbarpinned" : 0,
						"toptoolbarpinned" : 0,
						"righttoolbarpinned" : 0,
						"bottomtoolbarpinned" : 0,
						"toolbars_unpinned_last_save" : 0,
						"tallnewobj" : 0,
						"boxanimatetime" : 200,
						"enablehscroll" : 1,
						"enablevscroll" : 1,
						"devicewidth" : 0.0,
						"description" : "",
						"digest" : "",
						"tags" : "",
						"style" : "",
						"subpatcher_template" : "",
						"showontab" : 1,
						"assistshowspatchername" : 0,
						"boxes" : [ 							{
								"box" : 								{
									"id" : "obj-3",
									"maxclass" : "ezdac~",
									"numinlets" : 2,
									"numoutlets" : 0,
									"patching_rect" : [ 264.800000000000011, 496.0, 45.0, 45.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-2",
									"maxclass" : "button",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 609.0, 66.0, 24.0, 24.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-38",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 422.0, 629.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-34",
									"int" : 1,
									"maxclass" : "gswitch2",
									"numinlets" : 2,
									"numoutlets" : 2,
									"outlettype" : [ "", "" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 464.0, 186.0, 39.0, 32.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-33",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 413.0, 154.0, 59.0, 22.0 ],
									"text" : "random 3"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-32",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 422.0, 586.0, 29.5, 22.0 ],
									"text" : "-~"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-31",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 516.0, 517.0, 88.0, 22.0 ],
									"text" : "onepole~ 8000"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-30",
									"maxclass" : "newobj",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 422.0, 467.0, 29.5, 22.0 ],
									"text" : "*~"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-29",
									"maxclass" : "newobj",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 354.0, 410.0, 44.0, 22.0 ],
									"text" : "noise~"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-28",
									"maxclass" : "newobj",
									"numinlets" : 3,
									"numoutlets" : 2,
									"outlettype" : [ "signal", "bang" ],
									"patching_rect" : [ 435.0, 410.0, 45.0, 22.0 ],
									"text" : "curve~"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-27",
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 452.0, 317.0, 52.0, 20.0 ],
									"text" : "Closed"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-25",
									"maxclass" : "comment",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 543.0, 322.0, 43.0, 20.0 ],
									"text" : "Open"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-23",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 435.0, 344.0, 69.0, 22.0 ],
									"text" : "1, 0 $1 -0.9"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-22",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 517.0, 344.0, 69.0, 22.0 ],
									"text" : "1, 0 $1 -0.7"
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-20",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 526.0, 261.0, 50.0, 22.0 ],
									"text" : "311."
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-18",
									"maxclass" : "message",
									"numinlets" : 2,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 464.0, 261.0, 50.0, 22.0 ],
									"text" : "311."
								}

							}
, 							{
								"box" : 								{
									"format" : 6,
									"id" : "obj-15",
									"maxclass" : "flonum",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 585.0, 186.0, 50.0, 22.0 ]
								}

							}
, 							{
								"box" : 								{
									"format" : 6,
									"id" : "obj-13",
									"maxclass" : "flonum",
									"numinlets" : 1,
									"numoutlets" : 2,
									"outlettype" : [ "", "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 507.0, 186.0, 50.0, 22.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "newobj",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 311.0, 5.0, 42.0, 22.0 ],
									"text" : "r hihat"
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-18", 1 ],
									"order" : 1,
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-20", 1 ],
									"order" : 0,
									"source" : [ "obj-13", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-31", 1 ],
									"source" : [ "obj-15", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-23", 0 ],
									"source" : [ "obj-18", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-33", 0 ],
									"order" : 1,
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-34", 1 ],
									"order" : 0,
									"source" : [ "obj-2", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-22", 0 ],
									"source" : [ "obj-20", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-28", 0 ],
									"source" : [ "obj-22", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-28", 0 ],
									"source" : [ "obj-23", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-30", 1 ],
									"source" : [ "obj-28", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-30", 0 ],
									"source" : [ "obj-29", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-31", 0 ],
									"order" : 0,
									"source" : [ "obj-30", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-32", 0 ],
									"order" : 1,
									"source" : [ "obj-30", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-32", 1 ],
									"source" : [ "obj-31", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 1 ],
									"order" : 1,
									"source" : [ "obj-32", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-3", 0 ],
									"order" : 2,
									"source" : [ "obj-32", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-38", 0 ],
									"order" : 0,
									"source" : [ "obj-32", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-34", 0 ],
									"source" : [ "obj-33", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-18", 0 ],
									"source" : [ "obj-34", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-20", 0 ],
									"source" : [ "obj-34", 1 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-33", 0 ],
									"order" : 1,
									"source" : [ "obj-5", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-34", 1 ],
									"order" : 0,
									"source" : [ "obj-5", 0 ]
								}

							}
 ]
					}
,
					"patching_rect" : [ 608.0, 198.0, 45.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"globalpatchername" : "",
						"tags" : ""
					}
,
					"text" : "p hihat"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-14",
					"lastchannelcount" : 0,
					"maxclass" : "live.gain~",
					"numinlets" : 2,
					"numoutlets" : 5,
					"outlettype" : [ "signal", "signal", "", "float", "list" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 731.0, 286.0, 48.0, 136.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_longname" : "live.gain~[4]",
							"parameter_mmax" : 6.0,
							"parameter_mmin" : -70.0,
							"parameter_modmode" : 3,
							"parameter_shortname" : "live.gain~[1]",
							"parameter_type" : 0,
							"parameter_unitstyle" : 4
						}

					}
,
					"varname" : "live.gain~[3]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-13",
					"lastchannelcount" : 0,
					"maxclass" : "live.gain~",
					"numinlets" : 2,
					"numoutlets" : 5,
					"outlettype" : [ "signal", "signal", "", "float", "list" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 669.0, 290.0, 48.0, 136.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_longname" : "live.gain~[3]",
							"parameter_mmax" : 6.0,
							"parameter_mmin" : -70.0,
							"parameter_modmode" : 3,
							"parameter_shortname" : "live.gain~[1]",
							"parameter_type" : 0,
							"parameter_unitstyle" : 4
						}

					}
,
					"varname" : "live.gain~[2]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-12",
					"lastchannelcount" : 0,
					"maxclass" : "live.gain~",
					"numinlets" : 2,
					"numoutlets" : 5,
					"outlettype" : [ "signal", "signal", "", "float", "list" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 608.0, 286.0, 48.0, 136.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_longname" : "live.gain~[2]",
							"parameter_mmax" : 6.0,
							"parameter_mmin" : -70.0,
							"parameter_modmode" : 3,
							"parameter_shortname" : "live.gain~[1]",
							"parameter_type" : 0,
							"parameter_unitstyle" : 4
						}

					}
,
					"varname" : "live.gain~[1]"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-10",
					"lastchannelcount" : 0,
					"maxclass" : "live.gain~",
					"numinlets" : 2,
					"numoutlets" : 5,
					"outlettype" : [ "signal", "signal", "", "float", "list" ],
					"parameter_enable" : 1,
					"patching_rect" : [ 546.0, 286.0, 48.0, 136.0 ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_longname" : "live.gain~[1]",
							"parameter_mmax" : 6.0,
							"parameter_mmin" : -70.0,
							"parameter_modmode" : 3,
							"parameter_shortname" : "live.gain~[1]",
							"parameter_type" : 0,
							"parameter_unitstyle" : 4
						}

					}
,
					"varname" : "live.gain~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-11",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patcher" : 					{
						"fileversion" : 1,
						"appversion" : 						{
							"major" : 8,
							"minor" : 6,
							"revision" : 5,
							"architecture" : "x64",
							"modernui" : 1
						}
,
						"classnamespace" : "box",
						"rect" : [ 34.0, 113.0, 975.0, 689.0 ],
						"bglocked" : 0,
						"openinpresentation" : 0,
						"default_fontsize" : 12.0,
						"default_fontface" : 0,
						"default_fontname" : "Arial",
						"gridonopen" : 1,
						"gridsize" : [ 15.0, 15.0 ],
						"gridsnaponopen" : 1,
						"objectsnaponopen" : 1,
						"statusbarvisible" : 2,
						"toolbarvisible" : 1,
						"lefttoolbarpinned" : 0,
						"toptoolbarpinned" : 0,
						"righttoolbarpinned" : 0,
						"bottomtoolbarpinned" : 0,
						"toolbars_unpinned_last_save" : 0,
						"tallnewobj" : 0,
						"boxanimatetime" : 200,
						"enablehscroll" : 1,
						"enablevscroll" : 1,
						"devicewidth" : 0.0,
						"description" : "",
						"digest" : "",
						"tags" : "",
						"style" : "",
						"subpatcher_template" : "",
						"showontab" : 1,
						"assistshowspatchername" : 0,
						"boxes" : [ 							{
								"box" : 								{
									"id" : "obj-5",
									"maxclass" : "button",
									"numinlets" : 1,
									"numoutlets" : 1,
									"outlettype" : [ "bang" ],
									"parameter_enable" : 0,
									"patching_rect" : [ 385.0, 23.0, 24.0, 24.0 ]
								}

							}
, 							{
								"box" : 								{
									"comment" : "",
									"id" : "obj-4",
									"index" : 1,
									"maxclass" : "outlet",
									"numinlets" : 1,
									"numoutlets" : 0,
									"patching_rect" : [ 316.0, 623.0, 30.0, 30.0 ]
								}

							}
, 							{
								"box" : 								{
									"id" : "obj-3",
									"maxclass" : "newobj",
									"numinlets" : 0,
									"numoutlets" : 1,
									"outlettype" : [ "" ],
									"patching_rect" : [ 97.0, 9.0, 46.0, 22.0 ],
									"text" : "r snare"
								}

							}
, 							{
								"box" : 								{
									"bgmode" : 0,
									"border" : 0,
									"clickthrough" : 0,
									"enablehscroll" : 0,
									"enablevscroll" : 0,
									"id" : "obj-1",
									"lockeddragscroll" : 0,
									"lockedsize" : 0,
									"maxclass" : "bpatcher",
									"name" : "custom.snare.maxpat",
									"numinlets" : 2,
									"numoutlets" : 1,
									"offset" : [ 0.0, 0.0 ],
									"outlettype" : [ "signal" ],
									"patching_rect" : [ 155.0, 62.0, 649.0, 502.0 ],
									"viewvisibility" : 1
								}

							}
 ],
						"lines" : [ 							{
								"patchline" : 								{
									"destination" : [ "obj-4", 0 ],
									"source" : [ "obj-1", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-1", 0 ],
									"source" : [ "obj-3", 0 ]
								}

							}
, 							{
								"patchline" : 								{
									"destination" : [ "obj-1", 0 ],
									"source" : [ "obj-5", 0 ]
								}

							}
 ]
					}
,
					"patching_rect" : [ 546.0, 198.0, 49.0, 22.0 ],
					"saved_object_attributes" : 					{
						"description" : "",
						"digest" : "",
						"globalpatchername" : "",
						"tags" : ""
					}
,
					"text" : "p snare"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-55",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "", "", "" ],
					"patching_rect" : [ 123.5, 438.0, 56.0, 22.0 ],
					"restore" : 					{
						"live.gain~" : [ -0.00000000000001 ],
						"live.gain~[1]" : [ -9.88095238095238 ],
						"live.gain~[2]" : [ -5.315691208701995 ],
						"live.gain~[3]" : [ -6.037340693238097 ],
						"vst~" : [ 							{
								"filetype" : "C74Snapshot",
								"version" : 2,
								"minorversion" : 0,
								"name" : "kHs Compressor",
								"origin" : "kHs Compressor.auinfo",
								"type" : "AudioUnit",
								"subtype" : "AudioEffect",
								"embed" : 1,
								"snapshot" : 								{
									"pluginname" : "kHs Compressor.auinfo",
									"plugindisplayname" : "kHs Compressor",
									"pluginsavedname" : "C74_AU:/kHs Compressor",
									"pluginsaveduniqueid" : 711806331,
									"version" : 1,
									"isbank" : 0,
									"isbase64" : 1,
									"sliderorder" : [  ],
									"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1 ],
									"blob" : "802.hAGaoMGcv.i0AHv.DTfAGfPBJr.CT4VXsUFWsEla0YVXiQWcxUlbTQVXzEFUzkGbkc0b0IFc4AWYWYWYxMWZu41VDIWcsMGHPUmaiglDfrFRy8TDBXHTKM.AT..BHf..7nn3ZA...............n....vbzEFck4hZy8lasucxtsMLPX.3y1OEAD8Xgqk7Rc54dsn8dQgAC0HKBwEAtjfz.+tGRJIamkGg+KFPyO4vOReddY4Bl11PJ1Ot6kkKVvZnVdTE7Seuf8kvyCT5qqIesTef6HS33ImMNjiWOUmL7GTTStTvEoopZoQpk+erdKW4mChd5nx9zwAGIjdo0j95jTb7Iqqmm5s4C6PIEjorKQ+0rTz4bNyKaHQGWZtbCjkVXrl4NX35xM52ssSUtbIklgX3nWYCW63kPgUmX58VWYarSJ6CoC+iOUyAS2caSTwCo6Vdo+MWaQYC2tkqKZbWor.2chB4tedtzm93lpKhtGoa9WHUhqSOdg2VyaiNAU5XoxTeAFfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX.FfAX9TL4e+WIkYh5e8l4kKsukyShml2SSSa3ppsG1TeXeoorPmi7cVUyT15M0qqpNLF5x8JGTupptdy80aGqmm6wb4Ah2OsRRQb+3MXUpAUeupd2lwLdHvGG3vbz861tae89DsrLVdr.GeixKkZjg285vF3gtbkVtHXcO+se5hZ+c+IZDcq58hgwUMOYh2jNeDORt73QNeF9lhk46Rq0o4km4poySEOUlARV05c0yMQSA93694kuBTKc.BtXpww.f...v94...PsT.B...T..BHf..7nn3Z4hoFGC.B...6mC..n.......................LGcgQWYtn1bu4FTKUfA.....D..A..N....3H......RDVclgmDqM2XvAQ..f..U.fF.bB.r.PL.jC.AAPS.Hk.bKP3BXN.......f.A.........PC..................f.nC"
								}

							}
 ]
					}
,
					"text" : "autopattr",
					"varname" : "u392010283"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-8",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 9,
					"outlettype" : [ "int", "int", "float", "float", "float", "", "int", "float", "" ],
					"patching_rect" : [ 270.0, 45.0, 103.0, 22.0 ],
					"text" : "transport"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-39", 0 ],
					"order" : 1,
					"source" : [ "obj-1", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-46", 0 ],
					"order" : 0,
					"source" : [ "obj-1", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 1 ],
					"midpoints" : [ 562.75, 453.0, 836.5, 453.0 ],
					"source" : [ "obj-10", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 0 ],
					"midpoints" : [ 555.5, 453.0, 555.5, 453.0 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 1 ],
					"order" : 0,
					"source" : [ "obj-11", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"order" : 1,
					"source" : [ "obj-11", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 1 ],
					"midpoints" : [ 685.75, 453.0, 836.5, 453.0 ],
					"source" : [ "obj-13", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 0 ],
					"midpoints" : [ 678.5, 453.0, 555.5, 453.0 ],
					"source" : [ "obj-13", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 1 ],
					"midpoints" : [ 747.75, 453.0, 836.5, 453.0 ],
					"source" : [ "obj-14", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 0 ],
					"midpoints" : [ 740.5, 453.0, 555.5, 453.0 ],
					"source" : [ "obj-14", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 1 ],
					"order" : 0,
					"source" : [ "obj-16", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"order" : 1,
					"source" : [ "obj-16", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-13", 1 ],
					"order" : 0,
					"source" : [ "obj-18", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-13", 0 ],
					"order" : 1,
					"source" : [ "obj-18", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 1 ],
					"order" : 0,
					"source" : [ "obj-19", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"order" : 1,
					"source" : [ "obj-19", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-31", 0 ],
					"source" : [ "obj-23", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-34", 0 ],
					"source" : [ "obj-23", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-35", 0 ],
					"source" : [ "obj-23", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"source" : [ "obj-27", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 0 ],
					"source" : [ "obj-28", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-30", 0 ],
					"source" : [ "obj-29", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-2", 0 ],
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"source" : [ "obj-30", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-36", 0 ],
					"source" : [ "obj-31", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-23", 1 ],
					"source" : [ "obj-33", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-38", 0 ],
					"source" : [ "obj-34", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-37", 0 ],
					"source" : [ "obj-35", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-6", 0 ],
					"source" : [ "obj-43", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-47", 0 ],
					"source" : [ "obj-46", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-23", 0 ],
					"source" : [ "obj-47", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-49", 0 ],
					"source" : [ "obj-48", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 1 ],
					"source" : [ "obj-53", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-53", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-1", 0 ],
					"source" : [ "obj-6", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-22", 0 ],
					"source" : [ "obj-7", 0 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-10" : [ "live.gain~[1]", "live.gain~[1]", 0 ],
			"obj-11::obj-1::obj-104" : [ "live.toggle[1]", "live.toggle[1]", 0 ],
			"obj-11::obj-1::obj-70" : [ "live.gain~", "Gain", 0 ],
			"obj-12" : [ "live.gain~[2]", "live.gain~[1]", 0 ],
			"obj-13" : [ "live.gain~[3]", "live.gain~[1]", 0 ],
			"obj-14" : [ "live.gain~[4]", "live.gain~[1]", 0 ],
			"obj-18::obj-22" : [ "number[10]", "number[10]", 0 ],
			"obj-18::obj-28" : [ "vst~", "vst~", 0 ],
			"obj-18::obj-2::obj-12" : [ "button[3]", "button", 0 ],
			"obj-18::obj-2::obj-29" : [ "number[7]", "number", 0 ],
			"obj-18::obj-2::obj-39" : [ "live.toggle[4]", "live.toggle", 0 ],
			"obj-18::obj-2::obj-59" : [ "number[6]", "number[1]", 0 ],
			"obj-18::obj-2::obj-71" : [ "pitch[2]", "Pitch", 0 ],
			"obj-18::obj-2::obj-74" : [ "peakright[2]", "Peak Right", 0 ],
			"obj-18::obj-2::obj-77" : [ "peakdown[2]", "Peak Down", 0 ],
			"obj-18::obj-2::obj-79" : [ "snap[1]", "Snap", 0 ],
			"obj-18::obj-6" : [ "number", "number", 0 ],
			"obj-19::obj-2::obj-12" : [ "button[4]", "button", 0 ],
			"obj-19::obj-2::obj-29" : [ "number[9]", "number", 0 ],
			"obj-19::obj-2::obj-39" : [ "live.toggle[5]", "live.toggle", 0 ],
			"obj-19::obj-2::obj-59" : [ "number[8]", "number[1]", 0 ],
			"obj-19::obj-2::obj-71" : [ "pitch[3]", "Pitch", 0 ],
			"obj-19::obj-2::obj-74" : [ "peakright[3]", "Peak Right", 0 ],
			"obj-19::obj-2::obj-77" : [ "peakdown[3]", "Peak Down", 0 ],
			"obj-19::obj-2::obj-79" : [ "exponent[1]", "Exponent", 0 ],
			"obj-1::obj-6::obj-1" : [ "live.numbox[39]", "live.numbox[19]", 0 ],
			"obj-1::obj-6::obj-16" : [ "live.numbox[38]", "live.numbox[15]", 0 ],
			"obj-1::obj-6::obj-2" : [ "live.button[35]", "live.button", 0 ],
			"obj-1::obj-93::obj-25" : [ "live.button[16]", "live.button", 0 ],
			"obj-28::obj-12" : [ "note", "live.menu", 0 ],
			"obj-28::obj-19" : [ "waveform", "live.menu", 0 ],
			"obj-28::obj-22" : [ "scale", "rslider", 0 ],
			"obj-28::obj-25" : [ "duty", "Duty", 0 ],
			"obj-28::obj-5" : [ "rate", "Rate", 0 ],
			"obj-28::obj-6" : [ "live.toggle", "live.toggle", 0 ],
			"obj-43::obj-6::obj-10" : [ "live.numbox[89]", "live.numbox[2]", 0 ],
			"obj-43::obj-6::obj-12" : [ "live.text[6]", "live.text[2]", 0 ],
			"obj-43::obj-6::obj-2" : [ "live.button[3]", "live.button", 0 ],
			"obj-43::obj-6::obj-9" : [ "live.text[5]", "live.text[2]", 0 ],
			"obj-43::obj-93::obj-25" : [ "live.button[4]", "live.button", 0 ],
			"obj-53" : [ "vst~[1]", "vst~[1]", 0 ],
			"parameterbanks" : 			{
				"0" : 				{
					"index" : 0,
					"name" : "",
					"parameters" : [ "-", "-", "-", "-", "-", "-", "-", "-" ]
				}

			}
,
			"parameter_overrides" : 			{
				"obj-43::obj-93::obj-25" : 				{
					"parameter_longname" : "live.button[4]"
				}

			}
,
			"inherited_shortname" : 1
		}
,
		"dependency_cache" : [ 			{
				"name" : "Pause.svg",
				"bootpath" : "C74:/interfaces",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "Play.svg",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "custom.lfo.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/Custom Patches/patchers",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/Custom Patches/patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "custom.snare.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/Custom Patches/patchers",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/Custom Patches/patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "down.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "kHs Compressor.maxsnap",
				"bootpath" : "~/Documents/Max 8/Projects/Resonance/data",
				"patcherrelativepath" : "../../../../Documents/Max 8/Projects/Resonance/data",
				"type" : "mx@s",
				"implicit" : 1
			}
, 			{
				"name" : "kHs Compressor_20250620.maxsnap",
				"bootpath" : "~/Documents/Max 8/Projects/Resonance/data",
				"patcherrelativepath" : "../../../../Documents/Max 8/Projects/Resonance/data",
				"type" : "mx@s",
				"implicit" : 1
			}
, 			{
				"name" : "random.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "resize.js",
				"bootpath" : "~/Documents/Max 8/Packages/Custom Patches/patchers",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/Custom Patches/patchers",
				"type" : "TEXT",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.clock.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.clock.model.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.clock.view.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/clock",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.dist.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.dist.model.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.dist.presets.xml",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"type" : "TEXT",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.dist.view.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/modules/dist",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.module.attrchecker.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.module.control.js",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/javascript",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/javascript",
				"type" : "TEXT",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.module.control.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.module.remote.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "rtt.module.viewcontrol.maxpat",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/patchers/module-components",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "sine.svg",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "square.svg",
				"bootpath" : "~/Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"patcherrelativepath" : "../../../../Documents/Max 8/Packages/rhythm-and-time-toolkit/media/icons",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "up.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "updown.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
 ],
		"autosave" : 0
	}

}
